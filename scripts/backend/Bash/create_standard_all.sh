#! /bin/bash


hist_views_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
AND isCustom != 1
"
/cevac/scripts/exec_sql.sh "$hist_views_query" "standard_hist_views.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/standard_hist_views.csv
readarray tables_array < /cevac/cache/standard_hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  if [ -z "$t" ]; then
    continue
  fi
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`

  /cevac/scripts/seperator.sh
  /cevac/scripts/CREATE_ALL_VIEWS.sh "$B" "$M"

done


