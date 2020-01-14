#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

from setuptools import setup
import setuptools

with open("README", 'r') as f:
    long_description = f.read()

setup(name='CEVAC',
        version='0.0.1',
        description='The main CEVAC Python library',
        url='#',
        author='Bennett Meares',
        author_email='bmeares@g.clemson.edu',
        license='MIT',
        packages=setuptools.find_packages(),
        zip_safe=False,
        python_requires='>=3.6'
        )
