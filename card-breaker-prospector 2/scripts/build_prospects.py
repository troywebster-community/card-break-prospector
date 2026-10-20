#!/usr/bin/env python3
"""Compile audited public business prospect research JSONL to repeatable CSV exports."""
import argparse, csv, datetime as dt, json, re
from pathlib import Path
from urllib.parse import urlsplit

MAIN = ['Breaker / Brand','Whatnot / Fanatics / eBay','Instagram / YouTube','Audience size and promotion','Business Email','Email Source URL','Website / Linktree','SMS Program','Recent Activity','Priority Score','Email Status','Email Verification','Activity Source URL','SMS Source URL','Identity Source URL','Score Rationale','Research Date','Review Status','Notes']
EVID = ['Breaker / Brand','Claim Type','Claim Value','Source URL','Observed Date','Notes']
EMAIL = re.compile(r'^[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}$', re.I)


def valid_url(u):
    try:
        p = urlsplit(u)
        return p.scheme in ('http','https') and bool(p.netloc) and '.' in p.netloc
    except (ValueError,TypeError): return False


def date_parse(s):
    try: return dt.date.fromisoformat(s)
    except (ValueError, TypeError): return None


def score(r, today=None):
    today = today or dt.date.today()
    points=[]
    d=date_parse(r.get('activity_date',''))
    days=(today-d).days if d else None
    if days is not None and days >= 0 and valid_url(r.get('activity_source_url','')):
        n=25 if days<=14 else 18 if days<=45 else 8 if days<=90 else 0
        points.append(('dated activity',n))
    else: points.append(('dated activity',0))
    selling=r.get('selling') or {}; social=r.get('social') or {}
    points.append(('selling platforms',min(20,10*sum(valid_url(selling.get(x,'')) for x in ('whatnot','fanatics','ebay')))))
    points.append(('social profiles',min(10,5*sum(valid_url(social.get(x,'')) for x in ('instagram','youtube')))))
    audiences=r.get('audiences') or []
    top=max((int(a.get('followers') or 0) for a in audiences if valid_url(a.get('url','')) and date_parse(a.get('observed_date',''))),default=0)
    points.append(('reach',10 if top>=10000 else 5 if top>=1000 else 0))
    # Evidence requirement for promotion cadence, not just an unsourced classification.
    promotional_evidence=any(e.get('claim_type')=='promotion' and valid_url(e.get('url','')) for e in (r.get('evidence') or []))
    cadence=r.get('repeat_promotion','') if promotional_evidence else ''
    points.append(('promotion',15 if cadence=='recurring' else 5 if cadence=='single' else 0))
    published=bool(EMAIL.fullmatch(r.get('email','')) and valid_url(r.get('email_source_url','')))
    points.append(('contactability',15 if published else 5 if valid_url(r.get('contact_form_url','')) else 0))
    sms_yes=(r.get('sms_program')=='Yes' and valid_url(r.get('sms_source_url','')))
    points.append(('SMS opportunity',5 if sms_yes or r.get('sms_opportunity_observed') is True else 0))
    return sum(v for _,v in points), '; '.join(f'{k} {v}' for k,v in points)


def compact_links(d, pairs): return ' | '.join(f'{label}: {d[k]}' for k,label in pairs if valid_url(d.get(k,'')))


def identity(r):
    # Avoid false merges of brands with similar names. Merge only matching concrete URLs or identical brand names+same email domain.
    seller=r.get('selling') or {}; social=r.get('social') or {}
    urls=[seller.get(x,'') for x in ('whatnot','fanatics','ebay')]+[social.get(x,'') for x in ('instagram','youtube')]
    urls += [r.get('website',''),r.get('linktree','')]
    return {u.lower().rstrip('/') for u in urls if valid_url(u)}


def gather(inputdir):
    records=[]; errors=[]
    for path in sorted(inputdir.glob('*.jsonl')):
        for number,line in enumerate(path.read_text(encoding='utf8').splitlines(),1):
            if not line.strip(): continue
            try:
                obj=json.loads(line)
                if not isinstance(obj,dict) or not obj.get('brand'): raise ValueError('Missing brand/object')
                if obj['brand'].startswith('EXAMPLE ONLY'): continue
                obj['_file']=f'{path.name}:{number}'
                records.append(obj)
            except (json.JSONDecodeError,ValueError) as ex: errors.append(f'{path.name}:{number}: {ex}')
    return records,errors


def dedup(records):
    output=[]; notes=[]
    # Only collapse records where selling/social/official link URL overlaps, not name similarity.
    for r in records:
        matches=[p for p in output if identity(r) & identity(p)]
        if matches:
            p=matches[0]
            # Keep most thoroughly evidenced record rather than silently overwriting all claims.
            def richness(x): return len(x.get('evidence') or [])+len(identity(x))+(5 if x.get('email_source_url') else 0)
            if richness(r)>richness(p): output[output.index(p)]=r
            notes.append(f'Duplicate links: {r.get("brand")} ({r.get("_file")})')
        else: output.append(r)
    return output,notes


def build(records, today):
    prospects=[]; evidence=[]; review=[]
    for r in records:
        brand=r['brand'].strip(); selling=r.get('selling') or {}; social=r.get('social') or {}
        email=(r.get('email') or '').strip(); url=r.get('email_source_url') or ''
        good_email=bool(EMAIL.fullmatch(email) and valid_url(url))
        problems=[]
        if email and not good_email: problems.append('Email missing valid public source or format')
        if not valid_url(r.get('identity_source_url','')): problems.append('Identity source missing')
        if not identity(r): problems.append('No selling/social/website profile URL')
        if r.get('sms_program') not in ('Yes','No','Unknown'): problems.append('Invalid SMS status')
        if r.get('sms_program')=='Yes' and not valid_url(r.get('sms_source_url','')): problems.append('SMS Yes lacks source')
        if r.get('sms_program')=='No': problems.append('SMS No requires explicit absence evidence; review manually')
        d=date_parse(r.get('activity_date'))
        if d and d>today: problems.append('Activity date in future (scheduled vs actual activity?)')
        if d and not valid_url(r.get('activity_source_url','')): problems.append('Activity date has no source')
        if r.get('email_verification') not in (None,'Not checked','Deliverability verified','Failed'): problems.append('Invalid deliverability status')
        # Researcher/auditor flags for conflicting or weak evidence the checks above cannot see.
        problems += [str(x) for x in (r.get('review_flags') or []) if str(x).strip()]
        sc,rationale=score(r,today)
        audiences=[]
        for a in r.get('audiences') or []:
            if a.get('followers') is not None and valid_url(a.get('url','')) and date_parse(a.get('observed_date')):
                audiences.append(f'{a.get("platform", "Platform")}: {a["followers"]:,} (observed {a["observed_date"]})')
        promo='; '.join(filter(None,audiences+[r.get('promotion_description') or '']))
        row=dict(zip(MAIN,[brand,compact_links(selling,[('whatnot','Whatnot'),('fanatics','Fanatics Live'),('ebay','eBay Live')]),compact_links(social,[('instagram','Instagram'),('youtube','YouTube')]),promo,email if good_email else '',url if good_email else '', ' | '.join(x for x in (r.get('website',''),r.get('linktree','')) if valid_url(x)),r.get('sms_program') if r.get('sms_program') in ('Yes','No','Unknown') else 'Unknown',f'{d.isoformat()}: {r.get("activity_description", "")}' if d and d<=today and valid_url(r.get('activity_source_url','')) else '',sc,'Published' if good_email else 'Unverified' if email else 'Missing',r.get('email_verification') if good_email and r.get('email_verification') else 'Not checked',r.get('activity_source_url',''),r.get('sms_source_url',''),r.get('identity_source_url',''),rationale,r.get('research_date',''),'Needs review' if problems else 'Ready','; '.join(filter(None,[r.get('notes','')]+problems))]))
        prospects.append(row)
        for e in r.get('evidence') or []:
            evidence.append(dict(zip(EVID,[brand,e.get('claim_type',''),e.get('value',''),e.get('url',''),e.get('observed_date',''),e.get('notes','')])))
        if problems: review.append(row)
    prospects.sort(key=lambda x:(-x['Priority Score'],x['Breaker / Brand'].lower()))
    return prospects,evidence,review


def write_csv(path, cols, rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',default='data/input');parser.add_argument('--output',default='data/output');parser.add_argument('--as-of',default=dt.date.today().isoformat());a=parser.parse_args()
    today=date_parse(a.as_of)
    if not today: parser.error('--as-of must be YYYY-MM-DD')
    inputdir=Path(a.input);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    records,errors=gather(inputdir);unique,dups=dedup(records);prospects,evidence,review=build(unique,today)
    write_csv(out/'prospects.csv',MAIN,prospects);write_csv(out/'evidence.csv',EVID,evidence);write_csv(out/'review_queue.csv',MAIN,review)
    counts={'records':len(prospects),'published_business_emails':sum(p['Email Status']=='Published' for p in prospects),'verified_deliverability':sum(p['Email Verification']=='Deliverability verified' for p in prospects),'review_needed':len(review),'sms_yes':sum(p['SMS Program']=='Yes' for p in prospects),'with_recent_activity':sum(bool(p['Recent Activity']) for p in prospects),'duplicates_collapsed':len(dups),'parse_errors':len(errors)}
    summary='# Prospecting run summary\n\nAs of: '+today.isoformat()+'\n\n'+'\n'.join(f'- {k.replace("_"," ").capitalize()}: {v}' for k,v in counts.items())+'\n\n'
    summary+='## Warnings\n'+('\n'.join('- '+x for x in errors+dups) if errors+dups else '- None')+'\n\nNo records are generated without real research JSONL input. Published email is NOT deliverability verification.\n'
    (out/'run_summary.md').write_text(summary,encoding='utf8')
    print(summary)

if __name__=='__main__': main()
