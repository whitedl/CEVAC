#! /bin/bash
if [ -z "$1" ]; then
  echo Error: Missing table name
  echo "Usage: ./table_to_csv_append.sh [TABLE] [UTCDateTime] [Alias]"
  exit 1
fi
if [ -z "$2" ]; then
  echo "Error: Missing time metric (e.g. UTCDateTime)"
  echo "Usage: ./table_to_csv_append.sh [TABLE] [UTCDateTime] [Alias]"
  exit 1
fi
if [ -z "$3" ]; then
  echo "Error: Missing name metric (e.g. Alias)"
  echo "Usage: ./table_to_csv_append.sh [TABLE] [UTCDateTime] [Alias]"
  exit 1
fi

UTCDateTime="$2"
Alias="$3"

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
  WHERE $UTCDateTime > isnull(@begin, 0) AND $UTCDateTime <= @now
)
  INSERT INTO $table_CSV

  SELECT new.$UTCDateTime FROM new
  LEFT JOIN $table_CSV AS CSV ON CSV.$UTCDateTime = new.$UTCDateTime
  WHERE CSV.$UTCDateTime IS NULL

"
append_query="
SET NOCOUNT ON
DECLARE @begin DATETIME;
DECLARE @now DATETIME;
DECLARE @last_UTC DATETIME;
SET @now = GETUTCDATE();
SET @begin = DATEADD(day, -2, @now);
SET @last_UTC = (
  SELECT TOP 1 last_UTC FROM CEVAC_CACHE_RECORDS 
  WHERE table_name = '$table' AND storage = 'CSV'
  ORDER BY update_time DESC
);
IF DATEDIFF(day, @last_UTC, @begin) > 0 BEGIN
  SET @begin = @last_UTC;
END;

WITH new AS (
  SELECT * FROM $table
  WHERE $UTCDateTime > isnull(@begin, 0) AND $UTCDateTime <= @now
)
  SELECT new.* FROM new
  LEFT JOIN $table_CSV AS CSV ON CSV.$UTCDateTime = new.$UTCDateTime
  WHERE CSV.$UTCDateTime IS NULL
  ORDER BY LEN(new.$Alias) DESC
"


csv_utc_query="
SET NOCOUNT ON
IF OBJECT_ID('dbo.$table_CSV') IS NOT NULL DROP TABLE $table_CSV
SELECT $UTCDateTime
INTO $table_CSV
FROM $table
"
query="
SET NOCOUNT ON
SELECT * FROM $table
ORDER BY LEN($Alias) DESC
"
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

latest=$(echo $table | grep LATEST)
xref=$(echo $table | grep XREF)
if [ ! -z "$latest" ] || [ ! -z "$xref" ]; then
  echo LATEST or XREF detected. Will overwrite $table.csv
  rm -f /srv/csv/$table.csv
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

  if [ -z "$latest" ] && [ -z "$xref" ]; then
    echo "Creating $table_CSV..."
    /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$csv_utc_query"
  fi

  #append columns to beginning of CSV
  cat /home/bmeares/cache/cols_$table.csv /home/bmeares/cache/$table.csv > /home/bmeares/cache/temp_$table.csv && mv /home/bmeares/cache/temp_$table.csv /srv/csv/$table.csv
else # csv exists
  echo $table.csv found. Grabbing newest data...  

  echo Executing query:
  echo "$append_query"

  # Get columns and data
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$append_query" -W -o "/home/bmeares/cache/$table.csv" -s"," -w 700
  # remove separator
  sed 2d -i /home/bmeares/cache/$table.csv

  # get newest data since last download
  # /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$append_query" -W -o "/home/bmeares/cache/$table.csv" -h-1 -s"," -w 700
  rows_transferred=$(expr `wc -l < /home/bmeares/cache/$table.csv` - 1 )

  echo "Updating $table_CSV..."
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$csv_utc_append_query"

  echo Removing columns from /srv/csv/$table.csv...
  # remove columns from historical csv
#  sed -i '1d' /srv/csv/$table.csv
  tail -n +2 /srv/csv/$table.csv | sponge /srv/csv/$table.csv
  # append new data to top of existing csv
  # sed -i "1i`cat /home/bmeares/cache/$table.csv`" /srv/csv/$table.csv
  echo Appending data to existing $table.csv...
  cat /home/bmeares/cache/$table.csv /srv/csv/$table.csv | sponge /srv/csv/$table.csv
  echo Done appending.

  # append columns to cache CSV for Append
  # cat /home/bmeares/cache/cols_$table.csv /home/bmeares/cache/$table.csv > /home/bmeares/cache/temp_$table.csv && mv /home/bmeares/cache/temp_$table.csv /home/bmeares/cache/$table.csv

fi
echo Calculating row_count...
row_count=$(wc -l < /srv/csv/$table.csv)
record_query="
DECLARE @last_UTC DATETIME;
SET @last_UTC = (
  SELECT TOP 1 $UTCDateTime FROM $table
  ORDER BY $UTCDateTime DESC
);
INSERT INTO CEVAC_CACHE_RECORDS(table_name,update_time,storage,last_UTC,row_count,rows_transferred)
VALUES ('$table',GETUTCDATE(),'CSV', @last_UTC,($row_count - 1),$rows_transferred)
"

if [ -z "$xref" ]; then
  echo Inserting into CEVAC_CACHE_RECORDS
  # insert interaction into CEVAC_CACHE_RECORDS
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$record_query"
fi
echo Finished
