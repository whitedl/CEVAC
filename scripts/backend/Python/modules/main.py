#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
"""
from SQLConnector import SQLConnector
import json
from Table import Table
from AgeSet import AgeSet

def main():
    connector = SQLConnector()
    t = Table('WATT','TEMP','LATEST',connector)
    print(t.attributes['autoCACHE'])
    a = AgeSet('WATT','TEMP','HIST',connector)


if __name__ == "__main__":
    main()
