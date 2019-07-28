#! /bin/bash
error=""
views_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
"
if ! /cevac/scripts/exec_sql.sh "$views_query" "stats_views.csv" ; then
  error="Failed to get HIST_VIEW tables from CEVAC_TABLES"
  /cevac/scripts/log_error.sh "$error"
fi

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
  HIST="CEVAC_$B""_$M""_HIST"

  /cevac/scripts/seperator.sh
  echo "Calculating record counts for $HIST..."
  if ! /cevac/scripts/exec_sql.sh "EXEC CEVAC_RECORD_COUNTS @BuildingSName = '$B', @Metric = '$M'" ; then
    error="Error calulating record counts for $HIST"
    /cevac/scripts/log_error.sh "$error" "$HIST"
  fi

done


