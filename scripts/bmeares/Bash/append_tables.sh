#! /bin/bash

/cevac/scripts/seperator.sh

hist_views_query="
SELECT RTRIM(TableName) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
"
/cevac/scripts/exec_sql.sh "$hist_views_query" "hist_views.csv"

echo "Appending tables..."

# Remove header from csv
sed -i '1d' /cevac/cache/hist_views.csv
readarray tables_array < /cevac/cache/hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  if [ -z "$t" ]; then
    continue
  fi
  echo "$t"
  compare=$(echo "$t" | grep COMPARE)
  if [ -z "$compare" ]; then
    sql="EXEC CEVAC_CACHE_APPEND @tables = '"$t"'"
  else sql="EXEC CEVAC_CACHE_INIT @tables = '$t'"
  fi
  /cevac/scripts/exec_sql.sh "$sql"
  if [ ! $? -eq 0 ]; then
    echo "Error. Aborting append"
    exit 1
  fi
done


echo "Finished appending tables"
