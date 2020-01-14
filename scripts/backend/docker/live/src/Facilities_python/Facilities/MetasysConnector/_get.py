#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
import json
import urllib.parse
import requests
def get(self,rel,params={},full_url=None,raw=False):
    self.refresh_token()

    r_url = self.url + rel
    if full_url != None:
        r_url = full_url
    if params != {}:
        r_url += "?" + urllib.parse.urlencode(params)
        #  r_url += "?"
        #  first = True
        #  for k,v in params.items():
            #  if not first: r_url += "&"
            #  first = False
            #  r_url += str(k) + "=" + str(v)
    try:
        r = requests.get(r_url, headers=self.headers)
    except:
        print('Failed to get request:',r_url)
        return ""

    if raw:
        return r.text
    try:
        response_dict = json.loads(r.text)
    except:
        print('Failed to parse JSON')
        print('r_url: ', r_url)
        print('r.text:', r.text)
    else:
        return response_dict


