#! /bin/bash

if [ -z "$1" ]; then
  echo Error: Missing table name
  exit 1
fi

table="$1"
table_CSV="$table"_CSV
echo "table_CSV is $table_CSV"
cols_query="
SET NOCOUNT ON
SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('dbo.$table')"

csv_utc_append_query="
DECLARE @begin DATETIME;
DECLARE @now DATETIME;
SET @now = GETUTCDATE();
SET @begin = DATEADD(day, -2, @now);

WITH new AS (
  SELECT * FROM $table
  WHERE UTCDateTime > isnull(@begin, 0) AND UTCDateTime <= @now
)
  INSERT INTO $table_CSV

  SELECT new.UTCDateTime FROM new
  LEFT JOIN $table_CSV AS CSV ON CSV.UTCDateTime = new.UTCDateTime
  WHERE CSV.UTCDateTime IS NULL

"
append_query="
SET NOCOUNT ON
DECLARE @begin DATETIME;
DECLARE @now DATETIME;
SET @now = GETUTCDATE();
SET @begin = DATEADD(day, -2, @now);

WITH new AS (
  SELECT * FROM $table
  WHERE UTCDateTime > isnull(@begin, 0) AND UTCDateTime <= @now
)
  SELECT new.* FROM new
  LEFT JOIN $table_CSV AS CSV ON CSV.UTCDateTime = new.UTCDateTime
  WHERE CSV.UTCDateTime IS NULL
  ORDER BY UTCDateTime DESC
"


csv_utc_query="
SET NOCOUNT ON
IF OBJECT_ID('dbo.$table_CSV') IS NOT NULL DROP TABLE $table_CSV
SELECT UTCDateTime
INTO $table_CSV
FROM $table
"
query="
SET NOCOUNT ON
SELECT * FROM $table
ORDER BY UTCDateTime DESC
"
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

latest=$(echo $table | grep LATEST)
if [ ! -z $latest ]; then
  echo Latest table detected. Will overwrite $table.csv
fi

# If $table.csv doesn't exist, initialize data
if [ ! -f /srv/csv/$table.csv ] || [ ! -z $latest ]; then
  echo Generating $table.csv...
   # get columns
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$cols_query" -W -o "/home/bmeares/cache/cols_$table.csv" -h-1 -s"," -w 700
  tr '\n' ',' < /home/bmeares/cache/cols_$table.csv > /home/bmeares/cache/temp_cols_$table.csv && mv /home/bmeares/cache/temp_cols_$table.csv /home/bmeares/cache/cols_$table.csv
  truncate -s-1 /home/bmeares/cache/cols_$table.csv
  echo "" >> /home/bmeares/cache/cols_$table.csv

  echo Executing query:
  echo "$query"
  # get data
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -o "/home/bmeares/cache/$table.csv" -h-1 -s"," -w 700
  rows_transferred=$(wc -l < /home/bmeares/cache/$table.csv)

  echo "Creating $table_CSV..."
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$csv_utc_query"

  #append columns to beginning of CSV
  cat /home/bmeares/cache/cols_$table.csv /home/bmeares/cache/$table.csv > /home/bmeares/cache/temp_$table.csv && mv /home/bmeares/cache/temp_$table.csv /srv/csv/$table.csv
else # csv exists
  echo $table.csv found. Grabbing newest data...  

  echo Executing query:
  echo "$append_query"
  # get newest data since last download
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$append_query" -W -o "/home/bmeares/cache/$table.csv" -h-1 -s"," -w 700
  rows_transferred=$(wc -l < /home/bmeares/cache/$table.csv)

  echo "Updating $table_CSV..."
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$csv_utc_append_query"

  echo Appending data to existing $table.csv...
  # append new data to existing csv
  cat /home/bmeares/cache/$table.csv >> /srv/csv/$table.csv

fi
row_count=$(wc -l < /srv/csv/$table.csv)
record_query="
DECLARE @last_UTC DATETIME;
SET @last_UTC = (
  SELECT TOP 1 UTCDateTime FROM $table
  ORDER BY UTCDateTime DESC
);
INSERT INTO CEVAC_CACHE_RECORDS(table_name,update_time,storage,last_UTC,row_count,rows_transferred)
VALUES ('$table',GETUTCDATE(),'CSV', @last_UTC,($row_count - 1),$rows_transferred)
"

echo Inserting into CEVAC_CACHE_RECORDS
# insert interaction into CEVAC_CACHE_RECORDS
/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$record_query"
echo Finished
