#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

from setuptools import setup
import setuptools

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='Facilities',
   version='0.1.1',
   description='Access Metasys',
   long_description=long_description,
   author='Bennett Meares',
   author_email='bmeares@g.clemson.edu',
   packages=setuptools.find_packages(),  #same as name
   install_requires=['requests'],
   zip_safe=False,
   python_requires='>=3.6'
)
