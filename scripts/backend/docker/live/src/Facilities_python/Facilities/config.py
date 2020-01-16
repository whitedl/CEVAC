#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
This module stores passwords, hostnames, and other sensitive credentials.
"""
import yaml, sys
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

conf_path = 'config.yaml'
try:
    text = pkg_resources.read_text('Facilities',conf_path)
except:
    print(f'Unable to open {conf_path}. Does it exist?')
    raise FileNotFoundError

try:
    config = yaml.safe_load(text)
except:
    print(f'Unable to parse {conf_path}')
    sys.exit()
