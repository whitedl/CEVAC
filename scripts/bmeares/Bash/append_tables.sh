#! /bin/bash

/cevac/scripts/seperator.sh

hist_views_query="
SELECT RTRIM(TableName) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
"
/cevac/scripts/exec_sql.sh "$hist_views_query" "hist_views.csv"

echo "Appending HIST_CACHE tables..."

# Remove header from csv
sed -i '1d' /cevac/cache/hist_views.csv
readarray tables_array < /cevac/cache/hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  [ -z "$t" ] && continue
  echo "$t"
  compare=$(echo "$t" | grep COMPARE)
  if [ ! -z "$compare" ]; then # always recache COMPARE tables
    sql="EXEC CEVAC_CACHE_INIT @tables = '"$t"'"
  else sql="EXEC CEVAC_CACHE_APPEND @tables = '$t'"
  fi
  if ! /cevac/scripts/exec_sql.sh "$sql" ; then
    echo "Error. Aborting append"
    /cevac/scripts/log_error.sh "Error executing CEVAC_CACHE_APPEND" "$t"
    exit 1
  fi
done


echo "Finished appending HIST_CACHE tables"
