# For files
import json
import logging
from multiprocessing.dummy import current_process
import subprocess
import os
import re
from pathlib import Path

from random import random, choice  # more randomness
# For Sleeping
from time import time, sleep 

import requests
# For Souping
from torrequest import TorRequest
from requests import  request

#Souping things

# Hide me from Things
class HiddenRequest(TorRequest):
    """
    Sessions object that builds on both requests and Torrequests to include a VPN, randomized headers
    Each object has reset VPN and Tor
    VPNs can be disabled


    """
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.tor_session = TorRequest(**kwds)

        self.initial_ip = self._get_ip()

        self.proxy_off = False  # False for proxy is on (the requests won't verify otherwise)
        self.sleep_factor = 0

        self.requests_made = 0


    def _get_ip(self):
        """
            Gets the initial ip for the machine
        """
        try:
            ip = requests.get("https://ipinfo.io").json()['ip']
            print(f"My Original IP Address:{ip}")
        except Exception as cept:
            print(cept)
            logging.exception("Unable establish initial_ip. Restarting internet/vpn and reattempting...")
            try:
                self._disconnect_vpn()
                self._connect_to_vpn()
                ip = requests.get("https://ipinfo.io").json()['ip']
            except Exception as cept:
                print(cept)
                logging.critical("Unable to establish initial_ip. This will cause fatal error.")

        return ip

    def vpn_status(self):
        cmd = 'protonvpn s'
        result = subprocess.check_output(cmd,shell=True)
        if str(result).__contains__("Disconnected"):
            print(result)
            return False
        elif str(result).__contains__("Connected"):
            print(result)
            return True
        else:
            raise NotImplementedError

    def _disconnect_vpn(self):
        command = 'sudo protonvpn d'
        p = subprocess.check_output(command,shell=True)
        if str(p).__contains__("Disconnected") or str(p).__contains__("No connection found."):
            pass
        else:
            raise NotImplementedError

    def _connect_to_vpn(self):
        if self.vpn_status() is False:
            try:
                command = 'sudo protonvpn -r c'
                p = subprocess.check_output(command,shell=True)
            except Exception as e:
                print(e)
                logging.fatal("Exception: Failed to Initiate VPN Connection...disconnecting and reattempting")
                self._disconnect_vpn()
                raise NotImplementedError
   
    def get(self, *args, **kwargs):
        self._connect_to_vpn()
        self.requests_made += 1
        return self.tor_session.get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        self._connect_to_vpn()
        self.requests_made += 1
        return self.tor_session.post(*args, **kwargs)

    @staticmethod
    def pick_random_user_agent():
        user_agent_list = [
            # Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            # Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        user_agent = choice(user_agent_list)
        return user_agent

