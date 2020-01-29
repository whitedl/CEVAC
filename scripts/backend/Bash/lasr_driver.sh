#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
# /cevac/scripts/lock.sh

runsas="norun"
reset="append"
customLASR="0"
error=""
Age="HIST"

usage="Usage:
  -b BuildingSName
  -m Metric
  -l customLASR
  -s run SAS
  -r reset csv cache

  -h help
"
while getopts b:m:a:lsrh option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    a) Age=${OPTARG};;
    l) customLASR="1";;
    s) runsas="runsas";;
    r) reset="reset";;
    h) echo "$usage" && /cevac/scripts/unlock.sh && exit 1 ;;
  esac
done

if [ "$reset" == "reset" ]; then
  echo "Note: Reset detected. Loading entire HIST CSVs caches into LASR"
  echo "If you wish to rebuild CSV cache, delete everything in /srv/csv/"
  echo "If you wish to rebuild SQL cache, run ./init_tables.sh"
fi

# update HIST_CACHE tables
if [ "$Age" == "HIST" ]; then
  time if ! /cevac/scripts/append_tables.sh ; then
    error="Error updating HIST_CACHE tables"
    /cevac/scripts/log_error.sh "$error"
    # exit 1
  fi
fi

hist_views_query="
SELECT DISTINCT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE autoLASR = 1
AND Age LIKE '%$Age%'
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
    [ "$B" == "$A" ] && continue
    A="HIST_LASR"
    echo "Updating CEVAC_$B""_$M""_HIST_LASR"
    time if ! /cevac/scripts/CREATE_VIEW.sh "$B" "$M" "HIST_LASR"; then
      error="Error: Failed to create CEVAC_$B""_$M""_HIST_LASR"
      /cevac/scripts/log_error.sh "$error"
      continue
      # exit 1
    fi
  fi
  if [ "$A" == "LATEST" ]; then
    if ! /cevac/scripts/exec_sql.sh "EXEC CEVAC_LATEST_OR_LIVE @BuildingSName = '$B', @Metric = '$M'" ; then
      /cevac/scripts/log_error.sh "Failed to exec CEVAC_LATEST_OR_LIVE" "CEVAC_STATS_DT_INT"
      /cevac/scripts/unlock.sh
      exit 1
    fi
    q="SELECT TOP 1 newer_Age from CEVAC_STATS_DT_INT WHERE BuildingSName = '$B' AND Metric = '$M'"
    newer_Age=$(/cevac/scripts/sql_value.sh "$q")
    if [ "$newer_Age" != "$A" ] && [ ! -z "$newer_Age" ]; then
      echo "$newer_Age is newer than $A. Continue with $newer_Age instead? [Y/n] "
      # read answer
      answer="y"
      if [ "$answer" == "y" ] || [ "$answer" == "Y" ] || [ -z "$answer" ]; then
        A="$newer_Age"
        echo "Using $newer_Age instead of $A"
      fi
    fi
  fi

  /cevac/scripts/seperator.sh
  time if ! /cevac/scripts/lasr_append.sh $B $M $A "norun" $reset ; then
    error="Error uploading CEVAC_$B""_$M""_$A to LASR";
    /cevac/scripts/log_error.sh "$error"
    continue
    # exit 1
  fi
done
# wait
echo "All $Age tables have been loaded."
if [ "$runsas" == "runsas" ]; then
  echo "Executing runsas.sh..."
  time /cevac/scripts/runsas.sh
else
  echo "Skipping runsas.sh. Tables will be loaded automatically in 15 minutes."
fi

/cevac/scripts/unlock.sh

