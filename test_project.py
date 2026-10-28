from pathlib import Path
import os
import unittest
import json
import pandas as pd
from app import app, tableau_url
ROOT = Path(__file__).resolve().parent

class ProjectTests(unittest.TestCase):
    def test_metrics_reconcile(self):
        r=pd.read_csv(ROOT/'data/prepared/race_results.csv')
        d=pd.read_csv(ROOT/'data/prepared/driver_summary.csv')
        t=pd.read_csv(ROOT/'data/prepared/team_summary.csv')
        self.assertEqual(len(r),6464)
        self.assertEqual(r.points.sum(),d.points.sum())
        self.assertEqual(r.points.sum(),t.points.sum())
        self.assertEqual(r.dnf.sum(),396)
        self.assertEqual(r.race_driver_key.nunique(),len(r))
        self.assertTrue(r.loc[r.dnf.eq(1),'finish_position'].isna().all())
        self.assertEqual(r.race_id.nunique(),334)
        reconciliation=pd.read_csv(ROOT/'data/prepared/standings_reconciliation.csv')
        self.assertTrue(reconciliation.difference.eq(0).all())

    def test_missing_embed_is_honest(self):
        os.environ.pop('TABLEAU_DASHBOARD_URL',None)
        with app.test_client() as client:
            self.assertEqual(client.get('/').status_code,200)
            self.assertIn(b'awaiting publication',client.get('/').data)
            self.assertFalse(client.get('/health').json['tableau_configured'])
            self.assertEqual(client.get('/api/audit').json['metrics']['race_entries'],6464)

    def test_embed_url_validation(self):
        os.environ['TEST_URL']='javascript:alert(1)'
        with self.assertRaises(ValueError): tableau_url('TEST_URL')
        os.environ['TEST_URL']='https://public.tableau.com.evil.example/views/a/b'
        with self.assertRaises(ValueError): tableau_url('TEST_URL')
        os.environ['TEST_URL']='https://public.tableau.com/views/Workbook/Dashboard'
        self.assertEqual(tableau_url('TEST_URL'),os.environ['TEST_URL'])
        os.environ.pop('TEST_URL')

if __name__=='__main__': unittest.main()
