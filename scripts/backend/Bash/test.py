#! /usr/bin/python3

import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '130.127.218.11' 
database = 'WFIC-CEVAC' 
username = 'wficcm' 
password = '5wattcevacmaint$' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Sample select query
cursor.execute("SELECT * FROM test") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()
