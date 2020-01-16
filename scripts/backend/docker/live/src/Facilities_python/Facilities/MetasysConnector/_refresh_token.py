#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
import requests, datetime
import datetime
import pytz

def refresh_token(self):
    if pytz.utc.localize(datetime.datetime.utcnow()) > self.expires:
        r_url = self.url + 'refreshToken'
        try:
            r = requests.get(r_url,headers=self.headers)
        except:
            print('Failed to refresh token')
