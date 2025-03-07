#! /bin/bash

# ! /cevac/scripts/check_lock.sh && exit 1
# /cevac/scripts/lock.sh
if [ -z "$1" ]; then
  echo Error: Missing table name
  echo "Usage: $0 [TABLE] {reset}"
  /cevac/scripts/unlock.sh
  exit 1
fi
source /cevac/scripts/sql_env.sh
error=""
table="$1"
table_CSV="$table"_CSV
if [ ! -z "$2" ]; then
  if [ "$2" == "reset" ]; then
    echo "Reset! Removing /srv/csv/$table.csv"
    rm -f /srv/csv/$table.csv
    echo "Dropping $table_CSV"
    if ! /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL DROP TABLE $table_CSV" ; then
      error="Failed to drop $table_CSV"
      /cevac/scripts/log_error.sh "$error"
      exit 1
    fi
  fi
fi

table_CSV_exists_query="IF OBJECT_ID('$table_CSV') IS NOT NULL SELECT 'EXISTS' ELSE SELECT 'DNE'"
table_CSV_exists=`/cevac/scripts/sql_value.sh "$table_CSV_exists_query"`
xref=`echo $table | grep XREF`;

echo "$table_CSV_exists"
if [ "$table_CSV_exists" != "EXISTS" ] || [ ! -z "$xref" ]; then
  echo "$table_CSV does not exist. Removing local CSV"
  rm -f /srv/csv/$table.csv
else
  echo "$table_CSV exists in SQL. Will retain CSV if it exists"
fi


UTCDateTime=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE TableName = '$table'"`
Alias=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE TableName = '$table'"`
IDName=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(IDName) FROM CEVAC_TABLES WHERE TableName = '$table'"`
DataName=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(DataName) FROM CEVAC_TABLES WHERE TableName = '$table'"`

if [ -z "$UTCDateTime" ] || [ -z "$Alias" ] || [ -z "$DataName" ] || [ -z "$IDName" ]; then
  error="Tried to create $table_CSV without $table existing in CEVAC_TABLES"
  /cevac/scripts/log_error.sh "$error" "$table"
  exit 1
fi

echo "DateTimeName: $UTCDateTime"
echo "IDName: $IDName"
echo "AliasName: $Alias"
echo "DataName: $DataName"

cols_query="
SET NOCOUNT ON
SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('dbo.$table')"

cevac_tables_query="
IF EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = '$table') AND OBJECT_ID('$table_CSV') IS NOT NULL BEGIN
  DECLARE @BuildingSName NVARCHAR(MAX);
  DECLARE @Metric NVARCHAR(MAX);
  DECLARE @Age NVARCHAR(MAX);
  DECLARE @TableName NVARCHAR(MAX);
  DECLARE @DateTimeName NVARCHAR(MAX);
  DECLARE @AliasName NVARCHAR(MAX);
  DECLARE @IDName NVARCHAR(MAX);
  DECLARE @DataName NVARCHAR(MAX);
  DECLARE @isCustom BIT;
  DECLARE @customLASR BIT;
  SET @BuildingSName = (SELECT TOP 1 BuildingSName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @Metric = (SELECT TOP 1 Metric FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @Age = (SELECT TOP 1 Age FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @DateTimeName = (SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @IDName = (SELECT TOP 1 IDName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @AliasName = (SELECT TOP 1 AliasName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @DataName = (SELECT TOP 1 DataName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @isCustom = (SELECT TOP 1 isCustom FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @customLASR = (SELECT TOP 1 customLASR FROM CEVAC_TABLES WHERE TableName = '$table');
  

  DELETE FROM CEVAC_TABLES WHERE TableName = '$table_CSV';
  INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Dependencies, customLASR)
    VALUES (
      @BuildingSName,
      @Metric,
      @Age,
      '$table_CSV',
      '$UTCDateTime',
      '$IDName',
      '$Alias',
      '$DataName',
      @isCustom,
      '$table',
      @customLASR
    )
END
"

if [ "$UTCDateTime" != "$IDName" ]; then
  csv_new_cols="new.$UTCDateTime,new.$IDName"
else
  csv_new_cols="new.$UTCDateTime"
fi

csv_utc_append_query="
DECLARE @begin DATETIME;
DECLARE @now DATETIME;
DECLARE @update_time DATETIME;
SET @now = GETUTCDATE();
SET @begin = DATEADD(day, -31, @now);
SET @update_time = ISNULL((SELECT TOP 1 update_time FROM CEVAC_CACHE_RECORDS
  WHERE table_name = '$table' ORDER BY update_time DESC),0);

IF DATEDIFF(day, @update_time, @begin) > 0 SET @begin = DATEADD(day, -31,@update_time);

WITH new AS (
  SELECT * FROM $table
  WHERE $UTCDateTime > isnull(@begin, 0) AND $UTCDateTime <= @now
), new_csv AS (
  SELECT * FROM $table_CSV
  WHERE $UTCDateTime > isnull(@begin, 0) AND $UTCDateTime <= @now
)
  INSERT INTO $table_CSV

  SELECT $csv_new_cols
  FROM new
  LEFT JOIN new_csv AS CSV ON CSV.$UTCDateTime = new.$UTCDateTime AND CSV.$IDName = new.$IDName
  WHERE CSV.$UTCDateTime IS NULL

"
append_query="
SET NOCOUNT ON
DECLARE @begin DATETIME;
DECLARE @now DATETIME;
DECLARE @last_UTC DATETIME;
SET @now = GETUTCDATE();
SET @begin = DATEADD(day, -31, @now);
SET @last_UTC = (
  SELECT TOP 1 last_UTC FROM CEVAC_CACHE_RECORDS 
  WHERE table_name = '$table' AND storage = 'CSV'
  ORDER BY update_time DESC
);
IF DATEDIFF(day, @last_UTC, @begin) > 0 BEGIN
  SET @begin = DATEADD(DAY, -31, @last_UTC);
END;

WITH new AS (
  SELECT * FROM $table
  WHERE $UTCDateTime > isnull(@begin, 0) AND $UTCDateTime <= @now
), new_csv AS (
  SELECT * FROM $table_CSV
  WHERE $UTCDateTime > isnull(@begin, 0) AND $UTCDateTime <= @now
)
  SELECT new.* FROM new
  LEFT JOIN new_csv AS CSV ON CSV.$UTCDateTime = new.$UTCDateTime AND CSV.$IDName = new.$IDName
  WHERE CSV.$UTCDateTime IS NULL AND CSV.$IDName IS NULL
  ORDER BY LEN(new.$Alias) DESC
"

csv_utc_query="
SET NOCOUNT ON
IF OBJECT_ID('dbo.$table_CSV') IS NOT NULL DROP TABLE $table_CSV;
GO
SELECT $csv_new_cols
INTO $table_CSV
FROM $table AS new
"
query="
SET NOCOUNT ON
SELECT * 
FROM $table AS original
ORDER BY LEN(original.$Alias) DESC
"
h="$SQL_HOST"
u="$SQL_USER"
db="$SQL_DB"
p="$SQL_PASS"

hist=$(echo "$table" | grep "HIST")
latest=$(echo "$table" | grep "LATEST")
live=$(echo "$table" | grep "LIVE")
events=$(echo "$table" | grep "EVENTS")
xref=$(echo "$table" | grep "XREF")
issues=$(echo "$table" | grep "ISSUES")
compare=$(echo "$table" | grep "COMPARE")
lasr=$(echo "$table" | grep "LASR")
if [ ! -z "$latest" ] || [ ! -z "$xref" ] || [ ! -z "$compare"  ] || [ ! -z "$issues" ] || [ ! -z "$live" ] || [ ! -z "$events" ]; then
  echo LATEST, LIVE, XREF, COMPARE, or ISSUES detected. Will overwrite $table.csv
  rm -f /srv/csv/$table.csv
  echo "Dropping $table_CSV"
  if ! /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL DROP TABLE $table_CSV" ; then
    error="Cannot drop $table_CSV"
    /cevac/scripts/log_error.sh "$error" "$table_CSV"
    exit 1
  fi
fi

# If $table.csv doesn't exist, initialize data
if [ ! -f /srv/csv/$table.csv ]; then
  echo "/srv/csv/$table.csv doesn't exist"
  if ! /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL DROP TABLE $table_CSV"; then
    error="Failed to drop $table_CSV"
    /cevac/scripts/log_error.sh "$error" "$table_CSV"
    exit 1
  fi
  echo "Generating $table.csv..."
   # get columns
  rm -f /cevac/cache/cols_$table.csv
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$cols_query" -W -o "/cevac/cache/cols_$table.csv" -h-1 -s"," -w 700
  chmod 777 /cevac/cache/cols_$table.csv
  tr '\n' ',' < /cevac/cache/cols_$table.csv > /cevac/cache/temp_cols_$table.csv && mv /cevac/cache/temp_cols_$table.csv /cevac/cache/cols_$table.csv
  truncate -s-1 /cevac/cache/cols_$table.csv
  echo "" >> /cevac/cache/cols_$table.csv

  echo Executing query:
  echo "$query"
  # get data
  rm -f /cevac/cache/$table.csv
  if ! /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -o "/cevac/cache/$table.csv" -h-1 -s"," -w 700 ; then
    error="Failed generating $table.csv"
    /cevac/scripts/log_error.sh "$error" "$table"
    exit 1
  fi
  chmod 777 /cevac/cache/$table.csv
  if [ ! -z "$hist" ]; then
    # create _CSV if a HIST table
    if ! /cevac/scripts/exec_sql.sh "$csv_utc_query"; then
      error="Failed to create $table_CSV"
      /cevac/scripts/log_error.sh "$error" "$table"
      exit 1
    fi
  fi
  
  # Replace NULL with period for LASR
  sed -i 's/NULL/./g' /cevac/cache/$table.csv
  rows_transferred=$(wc -l < /cevac/cache/$table.csv)

  # append columns to beginning of CSV
  cat /cevac/cache/cols_$table.csv /cevac/cache/$table.csv > /cevac/cache/temp_$table.csv && mv /cevac/cache/temp_$table.csv /cevac/cache/$table.csv && cp /cevac/cache/$table.csv /srv/csv/$table.csv
else # csv exists
  echo "$table.csv found. Grabbing newest data...  "

  echo "Executing query:"
  echo "$append_query"

  # Get columns and data
  rm -f /cevac/cache/$table.csv
  if ! /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$append_query" -W -o "/cevac/cache/$table.csv" -s"," -w 700 ; then
    error="Failed to get columns and data..."
    /cevac/scripts/log_error.sh "$error" "$table"
    exit 1
  fi
  chmod 777 /cevac/cache/$table.csv
  # remove separator
  sed 2d -i /cevac/cache/$table.csv

  # get newest data since last download
  rows_transferred=$(expr `wc -l < /cevac/cache/$table.csv` - 1 )

  echo "Updating $table_CSV..."
  if ! /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$csv_utc_append_query" ; then
    error="Failed to append data to $table_CSV"
    /cevac/scripts/log_error.sh "$error" "$table_CSV"
    exit 1
  fi

  echo "Removing columns from /srv/csv/$table.csv..."
  # remove columns from historical csv
  tail -n +2 /srv/csv/$table.csv | sponge /srv/csv/$table.csv
  # append new data to top of existing csv
  echo "Appending data to existing $table.csv..."
  # Replace NULL with period for LASR
  sed -i 's/NULL/./g' /cevac/cache/$table.csv
  cat /cevac/cache/$table.csv /srv/csv/$table.csv | sponge /srv/csv/$table.csv
  chmod 777 /srv/csv/$table.csv
  echo "Done appending."

fi
echo "Calculating row_count..."
row_count=$(wc -l < /srv/csv/$table.csv)
record_query="
DECLARE @last_UTC DATETIME;
SET @last_UTC = (
  SELECT TOP 1 $UTCDateTime FROM $table
  ORDER BY $UTCDateTime DESC
);
INSERT INTO CEVAC_CACHE_RECORDS(table_name,update_time,storage,last_UTC,row_count,rows_transferred)
VALUES ('$table',GETUTCDATE(),'CSV', ISNULL(@last_UTC,0),($row_count - 1),$rows_transferred)
"

if [ -z "$xref" ]; then
  echo Inserting into CEVAC_CACHE_RECORDS
  # insert interaction into CEVAC_CACHE_RECORDS
  if ! /cevac/scripts/exec_sql.sh "$record_query" ; then
    error="Could not record csv interaction into CEVAC_CACHE_RECORDS for $table_CSV"
    /cevac/scripts/log_error.sh "$error" "$table_CSV"
    exit 1
  fi
fi

# echo "Adding to CEVAC_TABLES"
# echo "$cevac_tables_query" > /cevac/cache/CEVAC_TABLES_$table_CSV.sql
# if ! /cevac/scripts/exec_sql_script.sh "/cevac/cache/CEVAC_TABLES_$table_CSV.sql" ; then
  # error="Could not add $table_CSV to CEVAC_TABLES"
  # /cevac/scripts/log_error.sh "$error" "$table_CSV"
  # exit 1
# fi

echo "Finished updating /srv/csv/$table.csv"
# /cevac/scripts/unlock.sh
