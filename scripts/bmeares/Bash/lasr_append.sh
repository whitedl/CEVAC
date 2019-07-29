#! /bin/bash
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo Please enter building, metric, age.
  echo "Usage: $0 [BLDG] [METRIC] [AGE] {runsas} {reset}"
  exit 1
fi
building="$1"
metric="$2"
age="$3"
table="CEVAC_""$building""_""$metric""_""$age"
table_CSV="$table""_CSV"
error=""
if [ "$4" == "runsas" ]; then
  runsas="runsas"
fi
table_CSV_exists_query="IF OBJECT_ID('$table_CSV') IS NOT NULL SELECT 'EXISTS' ELSE SELECT 'DNE'"
table_CSV_exists=`/cevac/scripts/sql_value.sh "$table_CSV_exists_query"`
if [ "$5" == "reset" ] || [ ! -f /srv/csv/$table.csv ] || [ "$table_CSV_exists" != "EXISTS" ]; then
  reset="reset"
fi

dest_table=`python3 /cevac/python/name_shortener.py "$table"`
echo "LASR table will be called $dest_table"

echo "Creating $table.csv"

/cevac/scripts/table_to_csv_append.sh "$table"
if [ ! $? -eq 0 ]; then
  error="$table.csv failed. Aborting..."
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi
echo "Uploading CSV to LASR Autoloader..."

if [ "$reset" == "reset" ]; then
  echo "Reset detected. Uploading entire $table.csv"
  rsync -vh --progress /srv/csv/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad/$dest_table.csv
else
  echo "Sending newest lines of $table.csv over rsync..."
  rsync -vh --progress /cevac/cache/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad/Append/$dest_table.csv
fi

if [ "$runsas" == "runsas" ]; then
  echo "runsas detected. Executing LASR Autoload script..."
  /cevac/scripts/runsas.sh
  echo "Finished uploading to LASR"
else
  echo "runsas not detected. $table will be loaded into LASR on the next Autoload schedule"
fi


