import requests
import json
import hashlib
import enum
import logging
import pandas as pd
from datetime import time, datetime
from time import sleep
from collections import namedtuple
import os
import websocket
import rel
import ssl

from tradehub.base_validation.checksum import *
from config.config import *

import threading

logger = logging.getLogger(__name__)





class Trading:
    base_url = Props.base_url
    api_name = Props.api_name
    version = Props.pip_version
    base_url_c = Props.base_url_c

    _sub_urls = {
        # Authorization
        "getSessionData": Props.getSessionData,

        # OrderManagement
        "ordExecute": Props.ordExecute,
        "ordModify": Props.ordModify,
        "ordCancel": Props.ordCancel,
        "ordGetMargin": Props.ordGetMargin,
        "getOrderbook": Props.getOrderbook,
        "getTradebook": Props.getTradebook,
        "getOrdHistory": Props.getOrdHistory,

        # Portfolio
        "getHoldings": Props.getHoldings,
        "getPositions": Props.getPositions,
        "posConversion": Props.posConversion,

        # Funds
        "getFunds": Props.getFunds,

        # Profile
        "getProfile": Props.getProfile,

    }

    # Common Method
    def __init__(self,
                 user_id,
                 auth_Code,
                 secret_key,
                 base=None,
                 session_id=None):

        self.user_id = user_id.upper()
        self.auth_Code = auth_Code
        self.secret_key = secret_key
        self.session_id = session_id
        self.base = base or self.base_url
        self.__exchange_codes = None


    """API Request Module for POST and GET method"""
    def _request(self, method, req_type, data=None):
        """
        Headers with authorization. For some requests authorization
        is not required. It will be send as empty String
        """
        _headers = {
            "Authorization": self._user_authorization()
        }

        if req_type == "POST":
            try:
                response = requests.post(method, json=data, headers=_headers, )
            except (requests.ConnectionError, requests.Timeout) as exception:
                return {'stat': 'Not_ok', 'emsg': exception, 'encKey': None}
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                emsg = str(response.status_code) + ' - ' + response.reason
                return {'stat': 'Not_ok', 'emsg': emsg, 'encKey': None}

        elif req_type == "GET":
            try:
                response = requests.get(method, json=data, headers=_headers)
            except (requests.ConnectionError, requests.Timeout) as exception:
                return {'stat': 'Not_ok', 'emsg': exception, 'encKey': None}
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                emsg = str(response.status_code) + ' - ' + response.reason
                return {'stat': 'Not_ok', 'emsg': emsg, 'encKey': None}

    """1. API Methods declaration"""
    def _get(self, sub_url, data=None):
        """Get method declaration"""
        url = self.base + self._sub_urls[sub_url]
        return self._request(url, "GET", data=data)

    def _post(self, sub_url, data=None):
        """Post method declaration"""
        url = self.base + self._sub_urls[sub_url]
        print(url, data)
        return self._request(url, "POST", data=data)


    """1. API User Authorization"""
    def get_session_id(self, data=None):
        data = generate_checksum(self.user_id, self.auth_Code, self.secret_key)
        data = {'checkSum': data}

        response = self._post("getSessionData", data)

        """
        Extract accessToken from the response if status is 'Ok'.
        """
        if response.get('status') == 'Ok' and 'result' in response and len(response['result']) > 0:
            access_token = response['result'][0].get('accessToken')
            self.session_id = access_token

        return response

    def _user_authorization(self):
        if self.session_id:
            return "Bearer " + self.session_id
        else:
            return ""


    """GET Profile Records"""
    def get_profile(self):
        profile = self._get("getProfile")
        return profile

    """GET Funds Records"""
    def get_Funds(self):
        funds = self._get("getFunds")
        return funds

    """GET Orderbook Records"""
    def get_Orderbook(self):
        Orderbook = self._get("getOrderbook")
        return Orderbook

    """GET Tradebook Records"""
    def get_Tradebook(self):
        Tradebook = self._get("getTradebook")
        return Tradebook

    """GET Holdings Records"""
    def get_Holdings(self):
        Holdings = self._get("getHoldings")
        return Holdings

    """GET Positions Records"""
    def get_Positions(self):
        Positions = self._get("getPositions")
        return Positions