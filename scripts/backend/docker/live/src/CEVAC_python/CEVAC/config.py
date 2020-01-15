#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
This module stores passwords, hostnames, and other sensitive credentials.
"""
import yaml, sys, os

conf_path = 'config.yaml'
if not os.path.isfile(conf_path): conf_path = 'config.yml'
try:
    with open(conf_path) as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print(f'Unable to open {conf_path}. Does it exist?')
    raise
