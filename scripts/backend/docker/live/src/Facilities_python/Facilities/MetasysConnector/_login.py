#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import json
import requests
import dateutil.parser
from Facilities.config import config as cf

def login(self, username=cf['MetasysConnector']['username'], password=cf['MetasysConnector']['password']):
    headers = {'Content-Type': 'application/json'}
    data = '{"username": "' + username + '", "password": "' + password + '"}'
    r_url = self.url + 'login'
    r = requests.post(r_url, data=data, headers=headers)
    response_dict = json.loads(r.text)
    self.token = response_dict['accessToken']
    self.expires = dateutil.parser.parse(response_dict['expires'])
    self.headers = { 'Authorization': 'Bearer ' + self.token }

