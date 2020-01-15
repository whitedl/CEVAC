#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
from datetime import datetime
from config import config as cf

class MetasysConnector:
    from ._login import login
    from ._get import get
    from ._presentValue import presentValue
    from ._fqr_lookup import fqr_lookup
    from ._refresh_token import refresh_token
    from ._commands import getCommands
    from ._network import getNetworkDevices, getNetworkDeviceChildren, getNetworkDeviceChildrenObjects
    from ._trendedAttributes import getTrendedAttributes, getTrendedAttributeSamples
    def __init__(self,host=cf['MetasysConnector']['host']):
        self.token = ""
        self.expires = datetime.utcnow()
        self.host = host
        self.url = 'https://' + host + '/api/v2/'
        self.headers =  {}
        self.login()
