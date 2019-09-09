#! /bin/bash

usage="Usage:
  -b BuildingSName
  -m Metric
  -a Age
  -k keys_list
  -u unitOfMeasureID
  -h help
  -y run without asking
"
while getopts b:m:k:u:a:hycl option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    a) Age=${OPTARG};;
    k) keys_list=${OPTARG};;
    u) unitOfMeasureID=${OPTARG};;
    h) echo "$usage" && exit 1 ;;
    y) yes="yes";;
    l) autoLASR="true";;
    c) autoCACHE="true";;
  esac
done

hist_views_query="
SELECT RTRIM(TableName) AS 'TableName'
FROM CEVAC_TABLES
WHERE Age = '$Age'
AND TableName NOT LIKE '%CSV%'
"
/cevac/scripts/exec_sql.sh "$hist_views_query" "hist_views.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/hist_views.csv
readarray tables_array < /cevac/cache/hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  [ -z "$t" ] && continue
  query="
  INSERT INTO CEVAC_ALIAS_LOG(PointSliceID, Alias, UTCDateTime)
  SELECT PointSliceID, Alias, GETUTCDATE() AS 'UTCDateTime'
  FROM $t;
  "
  echo "$query"
  /cevac/scripts/exec_sql.sh "$query"

done



