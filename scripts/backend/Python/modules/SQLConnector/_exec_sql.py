#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import pandas as pd
def exec_sql(self, query):
    return pd.read_sql_query(query, self._connection)

    #  cursor = self.cursor()
    #  cursor.execute(query)
    #  rows = cursor.fetchall()
    #  l = []
    #  for r in rows:
        #  l.append(list(r))
    #  cursor.close()
    #  return l
