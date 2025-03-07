#! /bin/bash
usage="Usage:
  -b BuildingSName
  -m Metric

  -h help
"
while getopts b:m:k:u:hycl option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    h) echo "$usage" && exit 0 ;;
  esac
done
! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh


hist_views_query="
SELECT DISTINCT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age)
FROM CEVAC_TABLES
WHERE autoCACHE = 1
"
if [ ! -z "$BuildingSName" ]; then
  hist_views_query=$hist_views_query"
  AND BuildingSName = '"$BuildingSName"'"
fi
if [ ! -z "$Metric" ]; then
  hist_views_query=$hist_views_query"
  AND Metric = '"$Metric"'"
fi

/cevac/scripts/exec_sql.sh "$hist_views_query" "hist_views.csv"

echo "Appending HIST_CACHE tables..."

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

  TableName="CEVAC_$B""_$M""_$A"
  DAY="CEVAC_$B""_$M""_DAY"
  DAY_VIEW="CEVAC_$B""_$M""_DAY_VIEW"
  HIST="CEVAC_$B""_$M""_HIST"
  HIST_VIEW="CEVAC_$B""_$M""_HIST_VIEW"
  LATEST_FULL="CEVAC_$B""_$M""_LATEST_FULL"
  LATEST_BROKEN="CEVAC_$B""_$M""_LATEST_BROKEN"
  LATEST="CEVAC_$B""_$M""_LATEST"
  compare=$(echo "$TableName" | grep "COMPARE")
  pred=$(echo "$TableName" | grep "PRED")
  events=$(echo "$TableName" | grep "EVENTS")
  if [ ! -z "$compare" ] || [ ! -z "$pred" ] || [ ! -z "$events" ]; then # always recache COMPARE and PRED tables
    # sql="EXEC CEVAC_CACHE_INIT @tables = '"$HIST_VIEW"'; EXEC CEVAC_CACHE_INIT @tables = '$DAY_VIEW'"
    sql="EXEC CEVAC_CACHE_INIT @tables = '$HIST_VIEW,$DAY_VIEW,$LATEST_FULL,$LATEST,$LATEST_BROKEN'"
  else
    sql="EXEC CEVAC_CACHE_APPEND @tables = '$HIST_VIEW';
    EXEC CEVAC_CACHE_INIT @tables = '$DAY_VIEW,$LATEST_FULL,$LATEST,$LATEST_BROKEN'"
  fi
  if ! /cevac/scripts/exec_sql.sh "$sql" ; then
    echo "Error. Aborting append"
    /cevac/scripts/log_error.sh "Error executing CEVAC_CACHE_APPEND" "$TableName"
    # exit 1
  fi 
done


echo "Finished appending HIST_CACHE tables"
/cevac/scripts/unlock.sh
