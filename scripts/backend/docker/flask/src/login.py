#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
from flask import session

def logged_in():
    return 'username' in session
