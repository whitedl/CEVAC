#! /bin/sh


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
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 [BLDG] [METRIC] {keys_list} {unitOfMeasureID}"
  echo $'Enter the following information.\n'
  echo $'Building (e.g. WATT): '; read Building
  echo $'Metric   (e.g. TEMP): '; read Metric
  echo $'Keywords (e.g. SLAB,ZN-T,CRAC)\n     (empty to omit): '; read keys_list
  echo $'UnitOfMeasureID\n     (empty to omit): '; read unitOfMeasureID
fi

echo "Warning: This will completely rebuild the data pipeline and may take up to an hour."
echo "Custom tables WILL BE PRESERVED if CREATE_CUSTOM.sh has previously been run."
echo "Continue? (Y/n)"
read cont
if [ "$cont" != "y" ] || [ "$cont" != "Y" ] || [ -z "$cont" ]; then
  continue
else
  exit 1
fi

HIST="CEVAC_"$Building"_"$Metric"_HIST"
HIST_CACHE="CEVAC_"$Building"_"$Metric"_HIST_CACHE"
HIST_CSV="CEVAC_"$Building"_"$Metric"_HIST_CSV"
HIST_VIEW="CEVAC_"$Building"_"$Metric"_HIST_VIEW"
XREF="CEVAC_"$Building"_"$Metric"_XREF"

isCustom=`/cevac/scripts/sql_value.sh "SELECT isCustom FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
checkXREF=`/cevac/scripts/sql_value.sh "EXEC CHECK_XREF @BuildingSName = '$Building', @Metric = '$Metric'"`

if [ "$checkXREF" != "XREF" ]; then
  echo "WARNING: CEVAC_$Building""_$Metric""_XREF does not exist!"
  echo "You may continue bootstrapping with PointSliceID instead of Alias, but you MUST specify keywords or unitOfMeasureID"
  echo "CEVAC_$Building"_$Metric""_PXREF will be generated using the parameters provided during bootstrapping.""
  echo "  (Omitting parameters will include all PointSliceIDs for a building - so be careful!)"
fi

# isCustom is set, therefore exists
if [ ! -z "$isCustom" ]; then
  AliasName=`/cevac/scripts/sql_value.sh "SELECT AliasName FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  DateTimeName=`/cevac/scripts/sql_value.sh "SELECT DateTimeName FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  Dependencies=`/cevac/scripts/sql_value.sh "SELECT Dependencies FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  if [ "$isCustom" == "1" ]; then
    echo "Custom table detected. Please choose:"
    echo $'   1: Reuse previous table structure (no change)'
    echo $'   2: New table structure\n   (/cevac/CUSTOM_DEFS/$HIST_VIEW has changed)'
    read choice

    if [ "$choice" == "1" ]; then
      /cevac/scripts/CREATE_CUSTOM.sh "$Building" "$Metric" "$DateTimeName" "$AliasName" "$Dependencies"
    elif [ "$choice" == "2" ]; then
      /cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$Building' AND Metric = '$Metric'"
      echo "Executing CREATE_CUSTOM.sh"
      /cevac/scripts/CREATE_CUSTOM.sh
    else
      exit 1
    fi
    
  else # isCustom 0 or NULL, therefore standard table
    echo "Standard table detected"
    /cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$Building' AND Metric = '$Metric'"
  fi
else # isCustom does not exist therefore not in CEVAC_TABLES
  echo "New table (not located in CEVAC_TABLES)"
  if [ -f "/cevac/CUSTOM_DEFS/$HIST_VIEW.sql" ]; then # custom def exists
    echo "$HIST_VIEW is not in CEVAC_TABLES, but a custom definition was found in /cevac/CUSTOM_DEFS"
    echo "Choose one:"
    echo $'   1. Build custom   (   use /cevac/CUSTOM_DEFS/'$HIST_VIEW.sql")"
    echo $'   2. Build standard (ignore /cevac/CUSTOM_DEFS/'$HIST_VIEW.sql")"
    read choice
    if [ "$choice" == "1" ]; then # rebuild custom
      echo "Executing CREATE_CUSTOM.sh"
      /cevac/scripts/CREATE_CUSTOM.sh
    elif [ "$choice" == "2" ]; then
      continue
    fi

  fi
fi
###
# Phase 1: Drop caches
###
/cevac/scripts/seperator.sh
echo "Phase 1: Delete everything"
# Delete everything
/cevac/scripts/delete.sh $Building $Metric

###
# Phase 2: Create CEVAC tables system
###
/cevac/scripts/seperator.sh
echo "Phase: 2 create new views"
if ! /cevac/scripts/CREATE_ALL_VIEWS.sh $Building $Metric $keys_list $unitOfMeasureID ; then
  echo "Failed to create views. Aborting bootstrap"
  exit 1
fi

echo "CHECKPOINT 1"
/cevac/scripts/exec_sql.sh "CHECKPOINT"


###
# Phase 3: Init _CACHE
###
/cevac/scripts/seperator.sh
echo "Phase 4: init _CACHE"
time if ! /cevac/scripts/exec_sql.sh "EXEC CEVAC_CACHE_INIT @tables = '$HIST_VIEW'" ; then
  echo "CEVAC_CACHE_INIT failed. Aborting bootstrap"
  exit 1
fi

echo "CHECKPOINT 2"
/cevac/scripts/exec_sql.sh "CHECKPOINT"

###
# Phase 4: Rebuild /srv/csv/_HIST.csv
###
/cevac/scripts/seperator.sh
echo "Phase 4: create CSVs and rsync to LASR"
time /cevac/scripts/lasr_append.sh "$Building" "$Metric" HIST norun reset

echo "CHECKPOINT 3"
/cevac/scripts/exec_sql.sh "CHECKPOINT"

time /cevac/scripts/lasr_append.sh "$Building" "$Metric" LATEST norun reset
