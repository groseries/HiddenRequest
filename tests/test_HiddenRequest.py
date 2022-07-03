import unittest
import sys    
import os
import subprocess
from HiddenRequest import HiddenRequest

class TestHiddenRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = HiddenRequest()

    def tearDown(self) -> None:
        self.client.disconnect_vpn()

    def test_get_vpn_status(self):
        self.assertIs(bool,type(self.client.get_vpn_status()))

    def test_disconnect_vpn(self):
        self.client.disconnect_vpn()
        self.assertFalse(self.client.get_vpn_status())

    def test_connect_to_vpn(self):
        self.client.connect_to_vpn()
        self.assertTrue(self.client.get_vpn_status())

    def test_basic_get(self):
        self.client.get("https://www.google.com")
        
    
