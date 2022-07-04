# For files
from aifc import Error
import logging
from random import random
import subprocess
import requests
from torrequest import TorRequest
import randomheaders

class HiddenRequest(TorRequest):
    """
    Sessions object that builds on both requests and Torrequests to include a VPN and randomized headers

    """
    def __init__(self, **kwds):
        super().__init__( **kwds)
        self._public_ip_data = {}
        self._original_ip_data = {}
        self._get_original_ip_data()
    
    @property
    def random_header(self):
        return randomheaders.LoadHeader()

    @property
    def vpn_status(self):
        return self._get_vpn_status()
    
    @vpn_status.setter
    def vpn_status(self, value):
        if value is True:
            self._connect_to_vpn()
        elif value is False:
            self._disconnect_vpn()
        else:
            raise NotImplementedError("Value must be type bool to set status.")

    @property
    def public_ip_data(self):
        self._get_public_ip_data()
        return self._public_ip_data

    @public_ip_data.setter
    def public_ip_data(self, value):
        raise NotImplementedError("Cannot set public IP data manually.")

    @property
    def public_ip(self):
        if self.public_ip_data is None:
            self._get_public_ip_data()
        return self._public_ip_data['ip']

    @public_ip.setter
    def public_ip(self, value):
        raise NotImplementedError("Cannot set public IP  manually.")

    @property
    def original_ip_data(self):
        return self._original_ip_data
    
    @original_ip_data.setter
    def original_ip_data(self, value):
        raise NotImplementedError("Cannot set your own IP data manually.")

    @property
    def original_ip(self):
        return self._original_ip_data['ip']
    
    @original_ip.setter
    def original_ip(self, value):
        raise NotImplementedError("Cannot set your own IP manually.")
        


    def _get_public_ip_data(self):
        """
            Gets the public ip for the machine
        """
        if self.vpn_status is False:
            self._connect_to_vpn()
        try:
            self._public_ip_data = super().get("https://ipinfo.io").json()
        except Exception as cept:
            print(cept)
            logging.exception("Unable to find public ip data. Restarting internet/vpn and reattempting...")
            try:
                self._disconnect_vpn()
                self._connect_to_vpn()
                self._public_ip_data = super().get("https://ipinfo.io").json()
            except Exception as cept:
                print(cept)
                logging.critical("Unable to find public ip data. This will cause fatal error.")

    def _get_original_ip_data(self):
        if self.vpn_status is True:
            self._disconnect_vpn()
        try:
            self._original_ip_data = requests.get("https://ipinfo.io").json()
        except Exception as cept:
            print(cept)
            logging.exception("Unable find original ip data. Restarting internet/vpn and reattempting...")
            try:
                self._disconnect_vpn()
                self._connect_to_vpn()
                self._original_ip_data = requests.get("https://ipinfo.io").json()
            except Exception as cept:
                print(cept)
                logging.critical("Unable to find original_ip data. This will cause fatal error.")

    def _get_vpn_status(self):
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
        if self._get_vpn_status() is False:
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
        return super().get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        self._connect_to_vpn()
        return super().post(*args, **kwargs)

    def verify_hidden(self):
        if self.original_ip is self.public_ip:
            raise Error("Ip's are the same, you are not hidden.")
            return False
        if self.original_ip_data['hostname'] is self.public_ip_data['hostname']:
            raise Error("Your hostname is not hidden.")
            return False
        if self.original_ip_data['city'] is self.public_ip_data['city']:
            Warning("Your city is not hidden.")
            return False
        if self.original_ip_data['org'] is self.public_ip_data['org']:
            Warning("Your ISP is not hidden.")
            return False
        






