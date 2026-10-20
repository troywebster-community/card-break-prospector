# Research playbook for Claude Code

## Target
Independent and established sports/trading-card breakers with ongoing live-stream commerce. Prefer evidence published in the last 45 days; last 90 days may qualify at lower score. Cross-check each business rather than maximizing raw rows.

## Discovery searches (vary brands and geography)
- `"card breaks" "whatnot" "instagram"`
- `"sports card breaks" "business inquiries"`
- `"card breaks" "fanatics live" "schedule"`
- `site:linktr.ee "breaks" "whatnot"`
- `"card breaker" "youtube" "live"`
- `"card breaks" "text alerts"`
- `"case breaks" "email" "Instagram"`
- Seller search on Whatnot, Fanatics Live, eBay Live, YouTube and public social search where supported.

## Investigate each prospect
1. Find original public seller/store profile and record exactly which platform(s) actually sell breaks.
2. Follow explicitly cross-linked profiles, company-owned websites and link-in-bio pages.
3. Look for public sales/business inquiry email. Capture literal email and exact page URL, with observation date. If blocked or only a private identity is present, leave blank.
4. Capture dated promotional post or dated past/upcoming live-break event and source URL.
5. Identify public audience number only when visibly displayed and capture source evidence (platform, value, observed date). If no count, omit.
6. Look for opt-in SMS programs (text JOIN, official signup forms, 'text alerts' opt-in). Do not infer an existing program from posting a phone number.
7. Record recurring break schedules, and independently corroborate if ambiguous.
8. Add JSONL record as per schema example. Avoid duplicates by canonicalized brand AND confirmed shared platforms/domain, not name alone.

## Evidence collection
Each claim should appear in `evidence` as `{claim_type, value, url, observed_date, notes}`. Prefer `identity`, `seller`, `social`, `audience`, `promotion`, `activity`, `email`, `website`, `sms` claim types. Retain research date and say if pages are inaccessible.

## QA
- No empty brand names or source-less rows.
- Every email must have an exact email source URL and format check.
- SMS Yes requires source URL; SMS Unknown is default.
- All activity dates are exact and not future (future scheduled show is a promotion, distinguish it from a completed livestream).
- No simulated results. When research access is unavailable, stop with a clear diagnosis.
