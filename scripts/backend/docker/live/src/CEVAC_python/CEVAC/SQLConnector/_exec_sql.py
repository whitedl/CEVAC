#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import pandas as pd
import sqlalchemy
from sqlalchemy import text
def exec_sql(self, query):
    return pd.read_sql_query(query, self.engine)

def exec_only(self, query):
    try:
        with self.engine.connect() as conn:
            conn.execute(text(query).execution_options(autocommit=True))
    except Exception as e:
        print('Failed to execute query:\n' + query)
        print('Exception:')
        print(e)
    else:
        pass

def sql_value(self, query):
    df = pd.read_sql_query(query, self.engine)
    return df.iloc[0,0]

def to_sql(self, df, name='', if_exists='replace', index=False, dtype={}):
    df.to_sql(name, self.engine, if_exists=if_exists, index=index, dtype={})

