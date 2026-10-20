import unittest,sys,datetime as dt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_prospects import score, build, dedup

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.r={'brand':'Test Breaks','selling':{'whatnot':'https://whatnot.com/user/test'},'social':{'instagram':'https://instagram.com/test'},'activity_date':'2026-10-15','activity_source_url':'https://example.org/stream','identity_source_url':'https://whatnot.com/user/test','email':'sales@testbreaks.com','email_source_url':'https://testbreaks.com/contact','sms_program':'Unknown','research_date':'2026-10-20','evidence':[{'claim_type':'promotion','url':'https://example.org/schedule'}],'repeat_promotion':'recurring'}
    def test_scoring(self):
        value,_=score(self.r,dt.date(2026,10,20));self.assertEqual(value,70)
    def test_email_provenance(self):
        r={**self.r,'email_source_url':''};prospects,_,review=build([r],dt.date(2026,10,20));self.assertEqual(prospects[0]['Business Email'],'');self.assertEqual(prospects[0]['Email Status'],'Unverified');self.assertEqual(len(review),1)
    def test_dedup_links(self):
        r2={**self.r,'brand':'Different display name'};rows,notes=dedup([self.r,r2]);self.assertEqual(len(rows),1);self.assertEqual(len(notes),1)
    def test_sms_yes_needs_source(self):
        r={**self.r,'sms_program':'Yes'};_,_,review=build([r],dt.date(2026,10,20));self.assertEqual(len(review),1)
    def test_review_flags(self):
        r={**self.r,'review_flags':['Identity tied by name only']};prospects,_,review=build([r],dt.date(2026,10,20));self.assertEqual(len(review),1);self.assertIn('Identity tied by name only',prospects[0]['Notes'])

if __name__=='__main__': unittest.main()
