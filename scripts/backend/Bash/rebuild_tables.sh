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
BuildingSName="%"
Metric="%"
Age="%"
while getopts b:m:a:hy option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    a) Age=${OPTARG};;
    h) echo "$usage" && exit 1 ;;
    y) yes="yes";;
  esac
done

hist_views_query="
SELECT DISTINCT BuildingSName, Metric, 'PXREF' AS Age
FROM CEVAC_TABLES
WHERE Age LIKE '$Age'
AND BuildingSName LIKE '$BuildingSName'
AND Metric LIKE '$Metric'
AND TableName NOT LIKE '%CSV%'
"
/cevac/scripts/exec_sql.sh "$hist_views_query" "hist_views.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/hist_views.csv
readarray tables_array < /cevac/cache/hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  if [ -z "$t" ]; then
    continue
  fi
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`
  tableName="CEVAC_$B""_$M""_$A"
  /cevac/scripts/CREATE_VIEW.sh "$B" "$M" "$A"

done



