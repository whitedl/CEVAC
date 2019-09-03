#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

runsas="norun"
reset="append"
customLASR="0"
error=""
Age="HIST"

echo "Usage: $0 {customLASR} {runsas} {reset} {Age}"

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
if [ ! -z "$4" ]; then
  Age="$4"
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
if [ "$Age" == "HIST" ]; then
  time if ! /cevac/scripts/append_tables.sh ; then
    error="Error updating HIST_CACHE tables"
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi
fi

hist_views_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE autoLASR = 1
AND Age = '$Age'
AND customLASR = $customLASR
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
      continue
      # exit 1
    fi
  fi

  /cevac/scripts/seperator.sh
  time if ! { /cevac/scripts/lasr_append.sh $B $M $A $runsas $reset & } ; then
    error="Error uploading CEVAC_$B""_$M""_$A to LASR";
    /cevac/scripts/log_error.sh "$error"
    continue
    # exit 1
  fi
done
wait
echo "All _HIST tables have been loaded."
if [ "$runsas" != "norun" ]; then
  echo "Executing runsas.sh..."
  time /cevac/scripts/runsas.sh
else
  echo "Skipping runsas.sh. Tables will be loaded automatically in 15 minutes."
fi

/cevac/scripts/unlock.sh

