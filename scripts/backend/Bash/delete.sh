#! /bin/bash
usage="Usage:
  -b BuildingSName
  -m Metric
  -e Excluded Ages (comma-delimited; XREF and RAW always true)

  -h help
  -y run without asking
"
while getopts b:m:e:hy option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
		e) exclude_string=${OPTARG};;
    h) echo "$usage" && exit 1 ;;
    y) yes="yes";;
  esac
done

IFS=',' # comma is set as delimiter
read -ra exclude_array <<< "$exclude_string" # str is read into an array as tokens separated by IFS
IFS=' ' # reset to default value after usage

error=""
[ -z "$BuildingSName" ] && echo "BuildingSName  (e.g. WATT): " && read BuildingSName
[ -z "$Metric" ] && echo "Metric  (e.g. TEMP): " && read Metric
if [ -z "$BuildingSName" ] || [ -z "$Metric" ]; then exit 1; fi
LATEST="CEVAC_$BuildingSName""_$Metric""_LATEST"
HIST_VIEW="CEVAC_$BuildingSName""_$Metric""_HIST_VIEW"
HIST_CACHE="CEVAC_$BuildingSName""_$Metric""_HIST_CACHE"
HIST="CEVAC_$BuildingSName""_$Metric""_HIST"
HIST_LASR="CEVAC_$BuildingSName""_$Metric""_HIST_LASR"
echo "Warning: This will completely remove all traces of a BuildingSName/Metric"
echo "To recreate the tables, run bootstrap.sh (THIS MAY TAKE 1 HOUR)"
echo ""
echo "You are deleting all $BuildingSName""_$Metric tables (_RAW and _XREF will be ignored)"
echo "THIS CANNOT BE UNDONE. "
echo "Continue? (Y/n)"
if [ "$yes" != "yes" ]; then
  read cont
fi
if [ "$cont" != "y" ] && [ "$cont" != "Y" ] && [ ! -z "$cont" ]; then
  exit 1
fi

/cevac/scripts/log_activity.sh -t "$HIST"
isCustom=`/cevac/scripts/sql_value.sh "SELECT isCustom FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
exclude_array+=("RAW" "XREF")
exclude_query=""
# [ "$isCustom" == "1" ] && exclude_array+=('HIST_VIEW')
for a in "${exclude_array[@]}"; do
  exclude_query="$exclude_query
  AND Age NOT LIKE '%$a%'"
done

tables_query="
SELECT RTRIM(TableName) FROM CEVAC_TABLES
WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric' "$exclude_query"
"
echo "$tables_query"
/cevac/scripts/exec_sql.sh "$tables_query" "tables_temp.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/tables_temp.csv
readarray tables_array < /cevac/cache/tables_temp.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  t_CACHE=`echo "$t" | sed 's/VIEW/CACHE/g'`
  if [ -z "$t" ]; then
    continue
  fi
  table_type=`/cevac/scripts/sql_value.sh "SELECT TABLE_TYPE FROM information_schema.tables WHERE TABLE_NAME = '$t'"`
  table_type=$(echo "$table_type" | sed 's/BASE //g')

  sql="IF OBJECT_ID('$t') IS NOT NULL EXEC('DROP $table_type $t')"
  c_sql="IF OBJECT_ID('"$t_CACHE"') IS NOT NULL EXEC('DROP TABLE $t_CACHE')"
  if ! /cevac/scripts/exec_sql.sh "$sql"; then
    error="Error: Could not drop $t"
    /cevac/scripts/log_error.sh "$error" "$t"
    exit 1
  fi
  if ! /cevac/scripts/exec_sql.sh "$c_sql" ; then
    error="Error: Could not drop $t_CACHE"
    /cevac/scripts/log_error.sh "$error" "$t_CACHE"
    exit 1
  fi
done
# Drop HIST_CACHE just in case
sql="IF OBJECT_ID('$HIST_CACHE') IS NOT NULL EXEC('DROP TABLE $HIST_CACHE')"
if ! /cevac/scripts/exec_sql.sh "$sql"; then
  error="Error: Could not drop $t"
  /cevac/scripts/log_error.sh "$error" "$t"
  exit 1
fi

# Delete all from CEVAC_TABLES
if ! /cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric'""$exclude_query" ; then
  error="Error: Could not delete $BuildingSName"_$Metric" from CEVAC_TABLES"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

# Delete /srv/csv/_HIST.scv
rm -f /srv/csv/$HIST.csv
rm -f /srv/csv/$HIST_LASR.csv
rm -f /srv/csv/$LATEST.csv
dest_HIST=`python3 /cevac/CEVAC/scripts/importers/name_shortener.py $HIST`
dest_LATEST=`python3 /cevac/CEVAC/scripts/importers/name_shortener.py $HIST`
dest_HIST_LASR=`python3 /cevac/CEVAC/scripts/importers/name_shortener.py $HIST`
unload_command="[ -f ~/CEVAC/Autoload/$dest_HIST.csv ] && mv ~/CEVAC/Autoload/$dest_HIST.csv ~/CEVAC/Autoload/Unload/$dest_HIST.csv"
# ssh sas@wfic-sas-im-hd.clemson.edu "$unload_command"
unload_command="[ -f ~/CEVAC/Autoload/$dest_LATEST.csv ] && mv ~/CEVAC/Autoload/$dest_LATEST.csv ~/CEVAC/Autoload/Unload/$dest_LATEST.csv"
# ssh sas@wfic-sas-im-hd.clemson.edu "$unload_command"
unload_command="[ -f ~/CEVAC/Autoload/$dest_HIST_LASR.csv ] && mv ~/CEVAC/Autoload/$dest_HIST_LASR ~/CEVAC/Autoload/Unload/$dest_HIST_LASR.csv"
# ssh sas@wfic-sas-im-hd.clemson.edu "$unload_command"

sql="DELETE FROM CEVAC_ALL_LATEST_STATS WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric'"
if ! /cevac/scripts/exec_sql.sh "$sql" ; then
  error="Could not delete from CEVAC_ALL_LATEST_STATS"
  /cevac/scripts/exec_sql.sh "$error" "CEVAC_ALL_LATEST_STATS"
  exit 1
fi

echo "All $BuildingSName""_$Metric tables have been deleted."
