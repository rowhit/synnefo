#!/usr/bin/python
from commissioning.clients.http import main, HTTP_API_Client
from commissioning import QuotaholderAPI
import unittest

QH_URL = "http://localhost:8008/api/quotaholder/v"

class QuotaholderHTTP(HTTP_API_Client):
    api_spec = QuotaholderAPI()

class QuotaHolderAPITest(unittest.TestCase):
    def setUp(self):
        self.qh = QuotaholderHTTP(QH_URL)

    def tearDown(self):
        del self.qh

    def test_001_create_entity(self):
        pass

    def test_002_set_entity_key(self):
        pass

    def test_003_list_entities(self):
        pass

    def test_004_get_entity(self):
        pass

    def test_005_get_limits(self):
        pass

    def test_006_set_limits(self):
        pass

    def test_007_get_holding(self):
        pass

    def test_008_set_holding(self):
        pass

    def test_009_list_resources(self):
        pass

    def test_010_get_quota(self):
        pass

    def test_011_set_quota(self):
        pass

    def test_012_issue_commission(self):
        pass

    def test_013_accept_commission(self):
        pass

    def test_014_reject_commission(self):
        pass

    def test_015_get_pending_commissions(self):
        pass

    def test_016_resolve_pending_commissions(self):
        pass

    def test_017_release_entity(self):
        pass

    def test_018_get_timeline(self):
        pass



if __name__ == "__main__":
    unittest.main()
