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
    Torrequests has been disabled until I am able to get tor working on pi

    """
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.session = requests.Session()
        self.connected_to_vpn = self.get_vpn_status()
        self.connected_tor = False
        self.initial_ip = self._get_ip()
        self.max_req_tries = 4
        self.proxy_off = False  # False for proxy is on (the requests won't verify otherwise)
        self.sleep_factor = 0
        self.randomize_empty_headers = True
        # 1. Ensure VPN is connected
        self.connected_to_vpn = self.get_vpn_status()
       

    def _get_ip(self):
        """
            Gets the initial ip for the machine
        """
        try:
            initial_ip = requests.get("https://ipinfo.io").json()['ip']
            print("My Original IP Address:", initial_ip)
        except Exception as cept:
            print(cept)
            logging.exception("Unable establish initial_ip. Restarting internet/vpn and reattempting...")
            try:
                self.disconnect_vpn()
                self.connect_to_vpn()
                initial_ip = requests.get("https://ipinfo.io").json()['ip']
            except Exception as cept:
                print(cept)
                logging.critical("Unable to establish initial_ip. This will cause fatal error.")

        return initial_ip

    def get_vpn_status(self):
        cmd = 'protonvpn s'
        result = subprocess.check_output(cmd,shell=True)
        if str(result).__contains__("Disconnected"):
            self.connected_to_vpn=False
            return False
        else:
            self.connected_to_vpn=True
            return True

    def disconnect_vpn(self):
        command = 'protonvpn d'
        p = os.system('echo %s|sudo -S %s' % (self.sudo_pass, command))
        self.connected_to_vpn=False

    def connect_to_vpn(self):
        if self.connected_to_vpn is False:
            _vpnIP = self.initial_ip

            for i in range(0, self.max_req_tries):
                if _vpnIP == self.initial_ip:
                    try:
                        command = 'protonvpn -r c'
                        p = os.system('echo %s|sudo -S %s' % (self.sudo_pass, command))
                    except Exception as cept:
                        print(cept)
                        logging.exception("Exception: Failed to Initiate VPN Connection...disconnecting and reattempting")
                        self.disconnect_vpn()
                    
            if _vpnIP == self.initial_ip:
                logging.fatal("FAILED TO INITIATE VPN CONNECTION AFTER MULTIPLE ATTEMPTS... STOP RUNNING PROGRAM..."
                            "DATA IS EXPOSED THROUGH TOR REQUEST")
            self.connected_to_vpn=True
            return _vpnIP
   
    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    @staticmethod
    def _pick_random_user_agent():
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

