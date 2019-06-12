#! /bin/bash

if [ -z "$1" ]; then
  echo Error: Missing table name
  exit 1
fi

table="$1"
cols_query="
SET NOCOUNT ON
SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('dbo.$table')"
query="
SET NOCOUNT ON
SELECT * FROM $table"
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

# get columns
/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$cols_query" -W -o "/home/bmeares/cache/cols_$table.csv" -h-1 -s"," -w 700
tr '\n' ',' < /home/bmeares/cache/cols_$table.csv > /home/bmeares/cache/temp_cols_$table.csv && mv /home/bmeares/cache/temp_cols_$table.csv /home/bmeares/cache/cols_$table.csv
truncate -s-1 /home/bmeares/cache/cols_$table.csv
echo "" >> /home/bmeares/cache/cols_$table.csv

# get data
/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -o "/home/bmeares/cache/$table.csv" -h-1 -s"," -w 700

#append columns to beginning of CSV
cat /home/bmeares/cache/cols_$table.csv /home/bmeares/cache/$table.csv > /home/bmeares/cache/temp_$table.csv && mv /home/bmeares/cache/temp_$table.csv /srv/csv/$table.csv


echo Finished
