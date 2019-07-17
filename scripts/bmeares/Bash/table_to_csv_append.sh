#! /bin/bash
if [ -z "$1" ]; then
  echo Error: Missing table name
  echo "Usage: $0 [TABLE] {reset}"
  exit 1
fi
table="$1"
table_CSV="$table"_CSV
if [ -z "$2" ]; then
  if [ "$2" == "reset" ]; then
    echo "Reset! Removing /srv/csv/$table.csv"
    rm -f /srv/csv/$table.csv
    echo "Dropping $table_CSV"
    /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL DROP TABLE $table_CSV"
  fi
fi

table_CSV_exists_query="IF OBJECT_ID('$table_CSV') IS NOT NULL SELECT 'EXISTS' ELSE SELECT 'DNE'"
table_CSV_exists=`/cevac/scripts/sql_value.sh "$table_CSV_exists_query"`
if [ "$table_CSV_exists" != "EXISTS" ]; then
  echo "$table_CSV does not exist. Removing local CSV"
  rm -f /srv/csv/$table.csv
fi


UTCDateTime=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE TableName = '$table'"`
Alias=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE TableName = '$table'"`
DataName=`/cevac/scripts/sql_value.sh "SET NOCOUNT ON; SELECT TOP 1 RTRIM(DataName) FROM CEVAC_TABLES WHERE TableName = '$table'"`

if [ -z "$UTCDateTime" ] || [ -z "$Alias" ] || [ -z "$DataName" ]; then
  echo "Error: Missing DateTimeName, AliasName, or DataName for $table"
  echo "Enter the information below and rerun the script."
  echo "BuildingSName:"
  read BuildingSName
  echo "Metric:"
  read Metric
  echo "Age:"
  read Age
  echo "DateTimeName:"
  read DateTimeName
  echo "AliasName:"
  read AliasName
  echo "DataName:"
  read DataName

  failure_query="
  DECLARE @isCustom BIT;
  DECLARE @Definition NVARCHAR(MAX);
  SET @Definition = (SELECT TOP 1 Definition FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @isCustom = (SELECT TOP 1 isCustom FROM CEVAC_TABLES WHERE TableName = '$table');
	INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, DataName, isCustom, Definition)
		VALUES (
			'$BuildingSName',
			'$Metric',
			'$Age',
			'$table_CSV',
      '$DateTimeName',
      '$AliasName',
      '$DataName',
      @isCustom,
      @Definition
		)
  "
  /cevac/scripts/exec_sql.sh "$failure_query"
  echo "Inserted $table into CEVAC_TABLES"
  exit 1


fi

echo "DateTimeName: $UTCDateTime"
echo "AliasName: $Alias"
echo "DataName: $DataName"

cols_query="
SET NOCOUNT ON
SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('dbo.$table')"

cevac_tables_query="
IF EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = '$table') BEGIN
	DECLARE @BuildingSName NVARCHAR(100);
	DECLARE @Metric NVARCHAR(100);
	DECLARE @Age NVARCHAR(100);
	DECLARE @TableName NVARCHAR(100);
  DECLARE @DateTimeName NVARCHAR(50);
  DECLARE @AliasName NVARCHAR(50);
  DECLARE @DataName NVARCHAR(50);
	SET @BuildingSName = (SELECT TOP 1 BuildingSName FROM CEVAC_TABLES WHERE TableName = '$table');
	SET @Metric = (SELECT TOP 1 Metric FROM CEVAC_TABLES WHERE TableName = '$table');
	SET @Age = (SELECT TOP 1 Age FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @DateTimeName = (SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @AliasName = (SELECT TOP 1 AliasName FROM CEVAC_TABLES WHERE TableName = '$table');
  SET @DataName = (SELECT TOP 1 DataName FROM CEVAC_TABLES WHERE TableName = '$table');

	DELETE FROM CEVAC_TABLES WHERE TableName = '$table_CSV';
	INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, DataName)
		VALUES (
			@BuildingSName,
			@Metric,
			@Age,
			'$table_CSV',
      '$UTCDateTime',
      '$Alias',
      '$DataName'
		)
END

"

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

  SELECT new.$UTCDateTime, new.$Alias FROM new
  LEFT JOIN new_csv AS CSV ON CSV.$UTCDateTime = new.$UTCDateTime AND CSV.$Alias = new.$Alias
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
  LEFT JOIN new_csv AS CSV ON CSV.$UTCDateTime = new.$UTCDateTime
  WHERE CSV.$UTCDateTime IS NULL
  ORDER BY LEN(new.$Alias) DESC
"


csv_utc_query="
SET NOCOUNT ON
IF OBJECT_ID('dbo.$table_CSV') IS NOT NULL DROP TABLE $table_CSV;
GO
SELECT $UTCDateTime, $Alias
INTO $table_CSV
FROM $table
"
query="
SET NOCOUNT ON
SELECT * FROM $table AS original
ORDER BY LEN(original.$Alias) DESC
"
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

latest=$(echo "$table" | grep LATEST)
xref=$(echo "$table" | grep XREF)
compare=$(echo "$table" | grep COMPARE)
if [ ! -z "$latest" ] || [ ! -z "$xref" ] || [ ! -z "$compare"  ]; then
  echo LATEST, XREF, or COMPARE detected. Will overwrite $table.csv
  rm -f /srv/csv/$table.csv
  echo "Dropping $table_CSV"
  /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL DROP TABLE $table_CSV"
fi

# If $table.csv doesn't exist, initialize data
if [ ! -f /srv/csv/$table.csv ]; then
  /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL DROP TABLE $table_CSV"
  echo Generating $table.csv...
   # get columns
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$cols_query" -W -o "/cevac/cache/cols_$table.csv" -h-1 -s"," -w 700
  tr '\n' ',' < /home/bmeares/cache/cols_$table.csv > /home/bmeares/cache/temp_cols_$table.csv && mv /home/bmeares/cache/temp_cols_$table.csv /home/bmeares/cache/cols_$table.csv
  truncate -s-1 /home/bmeares/cache/cols_$table.csv
  echo "" >> /home/bmeares/cache/cols_$table.csv

  echo Executing query:
  echo "$query"
  # get data
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -o "/cevac/cache/$table.csv" -h-1 -s"," -w 700
  csv_error=`grep "Msg.*Level.*State.*Server" /cevac/cache/$table.csv`
  if [ ! -z "$csv_error" ]; then
    echo "Error: /cevac/cache/$table.csv failed."
    exit 1
  fi

  # Replace NULL with period for LASR
  sed -i 's/NULL/./g' /cevac/cache/$table.csv
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
  # Replace NULL with period for LASR
  sed -i 's/NULL/./g' /cevac/cache/$table.csv
  cat /home/bmeares/cache/$table.csv /srv/csv/$table.csv | sponge /srv/csv/$table.csv
  echo Done appending.

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
VALUES ('$table',GETUTCDATE(),'CSV', ISNULL(@last_UTC,0),($row_count - 1),$rows_transferred)
"

if [ -z "$xref" ]; then
  echo Inserting into CEVAC_CACHE_RECORDS
  # insert interaction into CEVAC_CACHE_RECORDS
  /cevac/scripts/exec_sql.sh "$record_query"
  # /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$record_query"
fi

echo "Adding to CEVAC_TABLES"
echo "$cevac_tables_query" > /cevac/cache/CEVAC_TABLES_$table_CSV.sql
/cevac/scripts/exec_sql_script.sh "/cevac/cache/CEVAC_TABLES_$table_CSV.sql"
# /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$cevac_tables_query"

echo Finished
