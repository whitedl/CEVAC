#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  from urllib.request import Request, urlopen
#  from urllib.parse import urlencode
import json
#  from json import dumps
import requests
#  import datetime
from dateutil import parser
from config import config as cf

def login(self, username=cf['MetasysConnector']['username'], password=cf['MetasysConnector']['password']):
    headers = {'Content-Type': 'application/json'}
    data = '{"username": "' + username + '", "password": "' + password + '"}'
    r_url = self.url + 'login'
    r = requests.post(r_url, data=data, headers=headers)
    response_dict = json.loads(r.text)
    self.token = response_dict['accessToken']
    self.expires = parser.parse(response_dict['expires'])
    self.headers = { 'Authorization': 'Bearer ' + self.token }

