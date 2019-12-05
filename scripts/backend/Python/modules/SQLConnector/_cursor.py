#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import pyodbc
"""

"""
#  @contextmanager
def cursor(self, commit: bool = False):
    """
    A context manager style of using a DB cursor for database operations. 
    This function should be used for any database queries or operations that 
    need to be done. 

    :param commit:
    A boolean value that says whether to commit any database changes to the database. Defaults to False.
    :type commit: bool
    """
    try:
        cursor = self._connection.cursor()
    except pyodbc.DatabaseError as err:
        print("DatabaseError {} ".format(err))
        cursor.rollback()
        raise err
    else:
        return cursor

