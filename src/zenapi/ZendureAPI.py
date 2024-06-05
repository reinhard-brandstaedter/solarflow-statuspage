'''
Zendure API used by the Mobile App. Handles log in and device info interfaces
'''

import os
import sys
import logging
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse

loglevel = os.environ.get("LOG_LEVEL", "info").upper()
FORMAT = '%(asctime)s:%(levelname)s: %(message)s'
logging.basicConfig(stream=sys.stdout, level=loglevel, format=FORMAT)
log = logging.getLogger(__name__)
PROD_NAME = os.environ.get('PROD_NAME','SolarFlow2.0')

SF_API_BASE_URL = "https://app.zendure.tech"

class ZendureAPI():
    ''' An API class to handle communication with the Zendure API '''

    def __init__(self, verifySSL=True, zen_api="https://app.zendure.tech/v2", parameters=None):
        self.baseUrl = f'{SF_API_BASE_URL}'
        self.zen_api = zen_api
        self.verifySSL = verifySSL
        self.parameters = parameters
        self.session = None

    def __enter__(self):
        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.verify = self.verifySSL
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.headers = {
                'Content-Type':'application/json',
                'Accept-Language': 'de-DE',
                'appVersion': '4.3.1',
                'User-Agent': 'Zendure/4.3.1 (iPhone; iOS 14.4.2; Scale/3.00)',
                'Accept': '*/*',
                'Authorization': 'Basic Q29uc3VtZXJBcHA6NX4qUmRuTnJATWg0WjEyMw==',
                'Blade-Auth': 'bearer (null)'
            }
        self.session.params = self.parameters
        return self

    def __exit__(self, type, value, traceback):
        self.session.close()
        self.session = None

    def authenticate(self, username, password):
        SF_AUTH_PATH = "/auth/app/token"
        authBody = {
                'password': password,
                'account': username,
                'appId': '121c83f761305d6cf7e',
                'appType': 'iOS',
                'grantType': 'password',
                'tenantId': ''
            }
        
        try:
            url = f'{self.zen_api}{SF_AUTH_PATH}'
            log.info("Authenticating with Zendure ...")
            response = self.session.post(url=url, json=authBody)
            if response.ok:
                respJson = response.json()
                token = respJson["data"]["accessToken"]
                #log.info(f'Got bearer token: {token}')
                self.session.headers["Blade-Auth"] = f'bearer {token}'
                return token
            else:
                log.error("Authentication failed!")
                log.error(response.text)
        except Exception as e:
            log.exception(e)

    def get_device_list(self):
        SF_DEVICELIST_PATH = "/productModule/device/queryDeviceListByConsumerId"
        try:
            url = f'{self.zen_api}{SF_DEVICELIST_PATH}'
            log.info("Getting device list ...")
            response = self.session.post(url=url)
            if response.ok:
                respJson = response.json()
                log.info(json.dumps(respJson["data"], indent=2))
                return respJson["data"]
            else:
                log.error("Fetching device list failed!")
                log.error(response.text)
        except Exception as e:
            log.exception(e)


    def get_device_ids(self):
        devices = self.get_device_list()
        ids = []
        for dev in devices:
            if dev["productName"] == f'{PROD_NAME}':
                ids.append(dev["id"])
        return ids


    def get_device_details(self, deviceId):
        SF_DEVICEDETAILS_PATH = "/device/solarFlow/detail"
        payload = {"deviceId": deviceId}
        try:
            url = f'{self.zen_api}{SF_DEVICEDETAILS_PATH}'
            log.info(f'Getting device details for [{deviceId}] ...')
            response = self.session.post(url=url, json=payload)
            if response.ok:
                respJson = response.json()
                log.info(json.dumps(respJson["data"], indent=2))
                return respJson["data"]
            else:
                log.error("Fetching device details failed!")
                log.error(response.text)
        except Exception as e:
            log.exception(e)
