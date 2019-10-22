#! /bin/bash

# ! /cevac/scripts/check_lock.sh && exit 1
# /cevac/scripts/lock.sh

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo Please enter building, metric, age.
  echo "Usage: $0 [BLDG] [METRIC] [AGE] {runsas} {reset}"
  # /cevac/scripts/unlock.sh
  exit 1
fi
building="$1"
metric="$2"
age="$3"
table="CEVAC_""$building""_""$metric""_""$age"
table_CSV="$table""_CSV"
/cevac/scripts/log_activity.sh -t "$table_CSV"
error=""
[ "$4" == "runsas" ] && runsas="runsas"

is_latest=`echo "$age" | grep "LATEST"`
if [ ! -z "$is_latest"  ]; then
  echo "Latest detected. Removing /srv/csv/$table.csv"
  rm -f /srv/csv/$table.csv
fi

table_CSV_exists_query="IF OBJECT_ID('$table_CSV') IS NOT NULL SELECT 'EXISTS' ELSE SELECT 'DNE'"
table_CSV_exists=`/cevac/scripts/sql_value.sh "$table_CSV_exists_query"`
if [ "$5" == "reset" ] || [ ! -f /srv/csv/$table.csv ] || [ "$table_CSV_exists" != "EXISTS" ]; then
  reset="reset"
fi

dest_table=`python3 /cevac/python/name_shortener.py "$table"`
echo "LASR table will be called $dest_table"

echo "Creating $table.csv"

if ! /cevac/scripts/table_to_csv_append.sh "$table" ; then
  error="$table.csv failed. Aborting..."
  /cevac/scripts/log_error.sh "$error" "$table"
  exit 1
fi

cat /cevac/cache/$table.csv >> /cevac/cache/upload_queue/$table.csv
echo "Uploading CSV to LASR Autoloader..."

if [ "$reset" == "reset" ]; then
  echo "Reset detected. Uploading entire $table.csv"
  if ! rsync -vh --progress /srv/csv/$table.csv sas@wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad/$dest_table.csv ; then
    error="Cannot rsync $table to LASR"
    /cevac/scripts/log_error.sh "$error" "$table"
    exit 1
  fi
else
  echo "Sending newest lines of $table.csv over rsync..."
  if ! rsync -vh --progress /cevac/cache/upload_queue/$table.csv sas@wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad/Append/$dest_table.csv ; then
    error="Cannot rsync cache to LASR"
    /cevac/scripts/log_error.sh "$error" "$table"
    exit 1
  else
    ## remove successfully uploaded cache files
    rm -f /cevac/cache/upload_queue/$table.csv
  fi
fi

if [ "$runsas" == "runsas" ]; then
  echo "runsas detected. Executing LASR Autoload script..."
  /cevac/scripts/runsas.sh
  echo "Finished uploading to LASR"
else
  echo "runsas not detected. $table will be loaded into LASR on the next Autoload schedule"
fi

# /cevac/scripts/unlock.sh
