#! /bin/sh

Building="$1"
Metric="$2"
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 [BLDG] [METRIC]"
  echo $'Enter the following information.\n'
  echo $'Building (e.g. WATT): '; read Building
  echo $'Metric   (e.g. TEMP): '; read Metric
fi

HIST_VIEW="CEVAC_$Building""_$Metric""_HIST_VIEW"
HIST="CEVAC_$Building""_$Metric""_HIST"
echo "Warning: This will completely remove all traces of a BuildingSName/Metric"
echo "To recreate the tables, run bootstrap.sh (THIS MAY TAKE > 1 HOUR)"
echo "Custom tables MUST be reconfigured with CREATE_CUSTOM.sh if recreated."
echo ""
echo "You are deleting all $Building""_$Metric tables (_RAW and _XREF will be ignored)"
echo "THIS CANNOT BE UNDONE. "
echo "Continue? (Y/n)"
read cont
if [ "$cont" != "y" ] || [ "$cont" != "Y" ] || [ -z "$cont" ]; then
  continue
else
  exit 1
fi
isCustom=`/cevac/scripts/sql_value.sh "SELECT isCustom FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
exclude_array=("RAW" "XREF")
exclude_query=""
[ "$isCustom" == "1" ] && exclude_array+=('HIST_VIEW')
for t in "${exclude_array[@]}"; do
  exclude_query="$exclude_query
  AND TableName NOT LIKE '%$t%'"
done

tables_query="
SELECT RTRIM(TableName) FROM CEVAC_TABLES
WHERE BuildingSName = '$Building' AND Metric = '$Metric' "$exclude_query"
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
  /cevac/scripts/exec_sql.sh "$sql"
  /cevac/scripts/exec_sql.sh "$c_sql"
done

# Delete all from CEVAC_TABLES
/cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$Building' AND Metric = '$Metric'""$exclude_query"

# Delete /srv/csv/_HIST.scv
rm -f /srv/csv/$HIST.csv

echo "All $Building""_$Metric tables have been deleted."
