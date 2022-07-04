import unittest
from src.HiddenRequest.HiddenRequest import HiddenRequest

class TestHiddenRequest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.client = HiddenRequest()

    def tearDown(self) -> None:
        self.client._disconnect_vpn()

    def test_disconnect_vpn(self):
        self.client._disconnect_vpn()
        self.assertFalse(self.client.vpn_status)
    
    def test_basic_get(self):
        self.client.get("https://www.google.com")

    def test_vpn_status(self):
        self.assertIs(bool,type(self.client.vpn_status))

    def test_connect_to_vpn(self):
        self.client._connect_to_vpn()
        self.assertTrue(self.client.vpn_status)

    def test_torrequest_get(self):
        r = self.client.get("https://www.google.com")
        self.assertEqual(r.status_code, 200)

    def test_HiddenRequest_session(self):
        with HiddenRequest() as hr:
            r = hr.get("https://www.google.com")
            self.assertTrue(hr.vpn_status)
            self.assertNotEqual(hr.original_ip, hr.public_ip)
        self.assertEqual(r.status_code, 200)
    
    def test_verify_hidden(self):
        self.client.verify_hidden()

        
        
        
    


    
        
    