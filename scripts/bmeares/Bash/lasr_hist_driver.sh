#! /bin/bash

runsas="norun"
reset="append"

if [ ! -z "$1" ]; then
  runsas="$1"
fi
if [ ! -z "$2" ]; then
  reset="$2"
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
# update HIST_CACHE tables
time /home/bmeares/scripts/append_tables.sh

hist_views_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE TableName LIKE '%HIST_VIEW%'
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

  /cevac/scripts/seperator.sh
  time /cevac/scripts/lasr_append.sh $B $M $A $runsas $reset

done

echo "All _HIST tables have been loaded."
if [ "$runsas" != "norun" ]; then
  echo "Executing runsas.sh..."
  time /home/bmeares/scripts/runsas.sh
else
  echo "Skipping runsas.sh. Tables will be loaded automatically in 15 minutes."
fi


