#! /bin/sh

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 [BLDG] [METRIC] {keys_list (optional)} {unitOfMeasureID (optional)}"
  exit 1
fi


keys_list="NULL"
unitOfMeasureID="NULL"

if [ ! -z "$3" ]; then
  keys_list="$3"
fi
if [ ! -z "$4" ]; then
  unitOfMeasureID="$4"
fi


Building="$1"
Metric="$2"
HIST="CEVAC_"$Building"_"$Metric"_HIST"
HIST_CACHE="CEVAC_"$Building"_"$Metric"_HIST_CACHE"
HIST_CSV="CEVAC_"$Building"_"$Metric"_HIST_CSV"
HIST_VIEW="CEVAC_"$Building"_"$Metric"_HIST_VIEW"

###
# Phase 1: Drop caches
###
# Drop _CACHE table
/cevac/scripts/seperator.sh
echo "Phase 1: Drop caches"
/cevac/scripts/exec_sql.sh "IF OBJECT_ID('$HIST_CACHE', 'U') IS NOT NULL DROP TABLE $HIST_CACHE"
# Drop _CSV table
/cevac/scripts/exec_sql.sh "IF OBJECT_ID('$HIST_CSV', 'U') IS NOT NULL DROP TABLE $HIST_CSV"
# Delete /srv/csv/_HIST.scv
rm -f /srv/csv/$HIST.csv

###
# Phase 2: Create new _VIEWs
###
/cevac/scripts/seperator.sh
echo "Phase: 2 create new views"
/cevac/scripts/CREATE_ALL_VIEWS.sh $Building $Metric $keys_list $unitOfMeasureID


echo "CHECKPOINT 1"
/cevac/scripts/exec_sql.sh "CHECKPOINT"



###
# Phase 3: Init _CACHE
###
/cevac/scripts/seperator.sh
echo "Phase 4: init _CACHE"
time /cevac/scripts/exec_sql.sh "EXEC CEVAC_CACHE_INIT @tables = '$HIST_VIEW'"

echo "CHECKPOINT 2"
/cevac/scripts/exec_sql.sh "CHECKPOINT"

###
# Phase 4: Rebuild /srv/csv/_HIST.csv
###
/cevac/scripts/seperator.sh
echo "Phase 4: create CSVs and rsync to LASR"
time /cevac/scripts/lasr_append.sh $Building $Metric HIST UTCDateTime Alias norun reset

echo "CHECKPOINT 3"
/cevac/scripts/exec_sql.sh "CHECKPOINT"

time /cevac/scripts/lasr_append.sh $Building $Metric LATEST UTCDateTime Alias norun reset
