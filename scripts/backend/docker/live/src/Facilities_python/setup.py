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
   version='0.1.4',
   description='Access Metasys',
   long_description=long_description,
   author='Bennett Meares',
   author_email='bmeares@g.clemson.edu',
   packages=setuptools.find_packages(),
   install_requires=['requests'],
   zip_safe=False,
   include_package_data=True,
   package_data={
       '' :['*.yaml','*.yml']
        },
   python_requires='>=3.6'
)
