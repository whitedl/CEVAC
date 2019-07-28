#! /bin/bash

runsas="norun"
reset="append"
customLASR="0"
error=""

echo "Usage: $0 {customLASR} {runsas} {reset}"

if [ ! -z "$1" ]; then
  echo "customLASR detected: Will only load HIST_LASR tables"
  customLASR="$1"
fi
if [ ! -z "$2" ]; then
  runsas="$2"
fi
if [ ! -z "$3" ]; then
  reset="$3"
fi
if [ "$reset" == "reset" ]; then
  echo "Note: Reset detected. Loading entire HIST CSVs caches into LASR"
  echo "If you wish to rebuild CSV cache, delete everything in /srv/csv/"
  echo "If you wish to rebuild SQL cache, run ./init_tables.sh"
fi
if [ "$runsas" == "runsas" ]; then
  echo "Note: runsas detected. Every table will trigger runsas.sh."
  echo "This may harm performance. Omit or use norun for argument 2 to only upload to LASR"
fi

hist_views_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
AND customLASR = $customLASR
AND TableName NOT LIKE '%SPACE%'
AND isCustom = 0
AND IDName IS NULL
"
/cevac/scripts/exec_sql.sh "$hist_views_query" "hist_views.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/hist_views.csv
readarray tables_array < /cevac/cache/hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  [ -z "$t" ] && continue
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`

  if [ "$customLASR" == "1" ]; then
    A="HIST_LASR"
    echo "Updating CEVAC_$B""_$M""_HIST_LASR"
    time if ! /cevac/scripts/CREATE_VIEW.sh "$B" "$M" "HIST_LASR"; then
      error="Error: Failed to create CEVAC_$B""_$M""_HIST_LASR"
      /cevac/scripts/log_error.sh "$error"
      exit 1
    fi
  fi

  /cevac/scripts/seperator.sh
  if ! /cevac/scripts/bootstrap.sh $B $M ; then
    error="Failed to bootstrap $B""_$M"
    /cevac/scripts/log_error.sh "$error"
  fi
done

if [ "$runsas" != "norun" ]; then
  echo "Executing runsas.sh..."
  time /cevac/scripts/runsas.sh
else
  echo "Skipping runsas.sh. Tables will be loaded automatically in 15 minutes."
fi

