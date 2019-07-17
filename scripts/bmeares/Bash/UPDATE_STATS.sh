#! /bin/bash

views_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
"
/cevac/scripts/exec_sql.sh "$views_query" "stats_views.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/stats_views.csv
readarray tables_array < /cevac/cache/stats_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  if [ -z "$t" ]; then
    continue
  fi
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`
  LATEST="CEVAC_$B""_$M""_LATEST"

  /cevac/scripts/seperator.sh
  echo "Calculating stats for $LATEST..."
  /cevac/scripts/exec_sql.sh "EXEC CEVAC_UPDATE_STATS @BuildingSName = '$B', @Metric = '$M'"
  if [ ! $? -eq 0 ]; then
    echo "Error calulating stats for $LATEST"
  fi

done


