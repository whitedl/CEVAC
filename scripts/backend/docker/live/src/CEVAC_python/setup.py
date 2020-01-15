#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

from setuptools import setup
import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='CEVAC',
        version='0.1.1',
        description='The main CEVAC Python library',
        url='#',
        author='Bennett Meares',
        author_email='bmeares@g.clemson.edu',
        license='MIT',
        packages=setuptools.find_packages(),
        zip_safe=False,
        package_data={
            '':['*.yaml','*.yml']
            },
        python_requires='>=3.6'
        )
