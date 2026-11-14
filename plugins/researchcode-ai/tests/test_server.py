import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server

class ResearchCodeTests(unittest.TestCase):
    def test_doi(self):
        self.assertEqual(server.clean_doi('https://doi.org/10.2307/12345'),'10.2307/12345')
        with self.assertRaises(server.ResearchError):server.clean_doi('http://evil.com')
    def test_ssrf(self):
        with self.assertRaises(server.ResearchError):server.fetch_json('http://169.254.169.254/latest')
        with self.assertRaises(server.ResearchError):server.fetch_json('https://example.org/data')
    def test_ranking_fails_closed(self):
        self.assertEqual(server.classify_journal('Journal of Accounting Research')['status'],'unverified')
        with self.assertRaises(server.ResearchError):server.search_publications('audit',tier='FT50')
    @patch.object(server,'fetch_json')
    def test_search(self,fake):
        fake.return_value={'results':[{'title':'Sample study','publication_year':2024,'doi':'https://doi.org/10.1234/abc',
             'primary_location':{'source':{'display_name':'Sample Journal'}},'open_access':{'is_oa':True},'id':'https://openalex.org/W1'}]}
        rows=server.search_publications('financial reporting',5)['results']
        self.assertEqual(rows[0]['open_code'],'not_assessed')
        self.assertEqual(rows[0]['ranking']['status'],'unverified')
        self.assertEqual(len(rows),1)
    @patch.object(server,'fetch_json')
    def test_replication_candidates_not_verified(self,fake):
        fake.side_effect=[{'hits':{'hits':[{'id':123,'metadata':{'title':'Data'}}]}}, {'data':{'items':[]}}]
        value=server.find_replication('10.1000/test')
        self.assertEqual(value['candidates'][0]['match_status'],'candidate_unverified')
    def test_reconciliation(self):
        self.assertTrue(server.reconciliation(110,100,[10])['mathematically_balanced'])
        self.assertFalse(server.reconciliation(110,100,[8])['mathematically_balanced'])
    def test_variance(self):
        self.assertEqual(server.variance_analysis(130,100)['percent_change'],'30.00')
        self.assertIsNone(server.variance_analysis(100,0)['percent_change'])
    def test_protocol(self):
        self.assertIn('tools',server.handle({'jsonrpc':'2.0','id':1,'method':'tools/list'})['result'])
        self.assertEqual(server.handle({'jsonrpc':'2.0','id':1,'method':'initialize'})['result']['serverInfo']['name'],'researchcode-ai')
        self.assertTrue(server.handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'variance_analysis','arguments':{'actual':1,'comparator':2}}})['result']['content'])
    def test_reject_unknown_arguments(self):
        x=server.handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'resolve_doi','arguments':{'doi':'10.1234/abc','url':'https://bad'}}})
        self.assertEqual(x['error']['code'],-32602)
    def test_negative_base_variance(self):
        self.assertEqual(server.variance_analysis(-20,-100)['percent_change'],'80.00')

if __name__=='__main__': unittest.main()
