#! /bin/bash

usage="Usage:
  -b BuildingSName
  -m Metric
  -k keys_list
  -u unitOfMeasureID

  -c cache tables
  -l load into LASR

  -h help
  -y run without asking
"
while getopts b:m:k:u:hycl option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    k) keys_list=${OPTARG};;
    u) unitOfMeasureID=${OPTARG};;
    h) echo "$usage" && exit 1 ;;
    y) yes="yes";;
    l) autoLASR="true";;
    c) autoCACHE="true";;
  esac
done
! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh
[ -z "$BuildingSName" ] && echo "BuildingSName (e.g. WATT): " && read BuildingSName
[ -z "$Metric" ] && echo "Metric (e.g. TEMP): " && read Metric
if [ -z "$yes" ]; then
  [ -z "$unitOfMeasureID" ] && echo "unitOfMeasureID (empty to omit): " && read unitOfMeasureID
  [ -z "$keys_list" ] && echo "keys_list (empty to omit): " && read keys_list
fi
echo "Warning: This will completely rebuild the data pipeline and may take up to an hour."
echo "Custom tables WILL BE PRESERVED if CREATE_CUSTOM.sh has previously been run."
echo "Continue? (Y/n)"
[ -z "$yes" ] && read cont
if [ "$cont" != "y" ] && [ "$cont" != "Y" ] && [ ! -z "$cont" ]; then
  /cevac/scripts/unlock.sh
  exit 1
fi

HIST="CEVAC_"$BuildingSName"_"$Metric"_HIST"
HIST_CACHE="CEVAC_"$BuildingSName"_"$Metric"_HIST_CACHE"
HIST_CSV="CEVAC_"$BuildingSName"_"$Metric"_HIST_CSV"
HIST_VIEW="CEVAC_"$BuildingSName"_"$Metric"_HIST_VIEW"
HIST_LASR="CEVAC_"$BuildingSName"_"$Metric"_HIST_LASR"
DAY="CEVAC_"$BuildingSName"_"$Metric"_DAY"
DAY_VIEW="CEVAC_"$BuildingSName"_"$Metric"_DAY_VIEW"
LATEST="CEVAC_"$BuildingSName"_"$Metric"_LATEST"
XREF="CEVAC_"$BuildingSName"_"$Metric"_XREF"
error=""

isCustom=`/cevac/scripts/sql_value.sh "SELECT isCustom FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
customLASR=`/cevac/scripts/sql_value.sh "SELECT customLASR FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
checkXREF=`/cevac/scripts/sql_value.sh "EXEC CHECK_XREF @BuildingSName = '$BuildingSName', @Metric = '$Metric'"`

# Parse XREF for setpoints
if [ "$checkXREF" != "XREF" ]; then
  echo "WARNING: CEVAC_$BuildingSName""_$Metric""_XREF does not exist!"
  echo "You may continue bootstrapping with PointSliceName instead of Alias, but if this is a standard table, you MUST specify keywords or unitOfMeasureID"
  echo "CEVAC_$BuildingSName"_$Metric""_PXREF will be generated using the parameters provided during bootstrapping.""
  echo "  (Omitting parameters for XREF-less standard tables will include all PointSliceIDs for a building - so be careful!)"
else
  xref_readingType=`/cevac/scripts/sql_value.sh "IF 'ReadingType' IN (SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$XREF') SELECT 'ReadingType' ELSE SELECT 'No ReadingType'"`
  # See if ReadingType is in XREF. If so, see if Set Points exist
  if [ "$xref_readingType" == "ReadingType" ]; then
    check_customLASR=`/cevac/scripts/sql_value.sh "IF EXISTS(SELECT TOP 1 * FROM $XREF WHERE ReadingType LIKE '%SP%') SELECT 'LASR' ELSE SELECT 'STANDARD'"`
  else
    check_customLASR="0"
  fi
  if [ "$customLASR" == "1" ] || [ "$check_customLASR" == "LASR" ]; then
    echo "customLASR: $customLASR"
    echo "check_customLASR: $check_customLASR"
    echo "Set points detected in XREF. Create HIST_LASR table? (~5 extra minutes) (Y/n)"
    if [ -z "$yes" ]; then
      read choice
    else
      choice=""
    fi
    if [ "$choice" == "y" ] || [ "$choice" == "Y" ] || [ -z "$choice" ]; then
      customLASR="1"
      echo "Will create $HIST_LASR"
    fi
  fi
fi

## isCustom is set, therefore exists in CEVAC_TABLES
if [ ! -z "$isCustom" ]; then
  IDName=`/cevac/scripts/sql_value.sh "SELECT IDName FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  AliasName=`/cevac/scripts/sql_value.sh "SELECT AliasName FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  DataName=`/cevac/scripts/sql_value.sh "SELECT DataName FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  DateTimeName=`/cevac/scripts/sql_value.sh "SELECT DateTimeName FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  Dependencies=`/cevac/scripts/sql_value.sh "SELECT Dependencies FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
  if [ "$isCustom" == "1" ]; then
    echo "Custom table detected. Please choose:"
    echo $'   1: Reuse previous table structure (no change) (empty to default)'
    echo $'   2: New table structure\n   (/cevac/CUSTOM_DEFS/'"$HIST_VIEW"' has changed)'
    if [ -z "$yes" ]; then
      read choice
    else
      choice=""
    fi
    ## Detected a custom table but decided to disregard
    if [ "$choice" == "2" ]; then
      echo "Dropping caches..."
      /cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric'"
      /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$HIST_CACHE') IS NOT NULL DROP TABLE $HIST_CACHE;"
      /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$HIST_CSV') IS NOT NULL DROP TABLE $HIST_CSV;"
      /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$HIST_LASR') IS NOT NULL DROP TABLE $HIST_LASR;"
      echo "Executing CREATE_CUSTOM.sh"
      if ! /cevac/scripts/CREATE_CUSTOM.sh ; then
        error="Error creating custom"
        /cevac/scripts/log_error.sh "$error"
        exit 1
      fi
    ## Exit on invalid answer
    elif [ "$choice" != "1" ] && [ "$choice" != "" ]; then
      /cevac/scripts/unlock.sh
      exit 1
    fi
  
  else # isCustom 0 or NULL, therefore standard table
    echo "Standard table detected"
    # if ! /cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric'" ; then
      # error="Error: could not delete $BuildingSName""_""$Metric from CEVAC_TABLES. Aborting bootstrap..."
      # /cevac/scripts/log_error.sh "$error"
      # exit 1
    # fi
  fi ## end of isCustom == 1
else ## isCustom does not exist therefore not in CEVAC_TABLES
  echo "New table (not located in CEVAC_TABLES)"
  if [ -f "/cevac/CUSTOM_DEFS/$HIST_VIEW.sql" ]; then # custom def exists
    echo "$HIST_VIEW is not in CEVAC_TABLES, but a custom definition was found in /cevac/CUSTOM_DEFS/"
    echo "Choose one:"
    echo $'   1. Build custom   (   use /cevac/CUSTOM_DEFS/'$HIST_VIEW.sql")"
    echo $'   2. Build standard (ignore /cevac/CUSTOM_DEFS/'$HIST_VIEW.sql")"
    if [ -z "$yes" ]; then
      read choice
    else
      choice=""
    fi
    if [ "$choice" == "1" ] || [ "$choice" == "" ]; then # rebuild custom
      echo "Executing CREATE_CUSTOM.sh"
      if ! /cevac/scripts/CREATE_CUSTOM.sh "$BuildingSName" "$Metric" ; then
        error="Error: Could not create $HIST_VIEW as a custom table. Aborting bootstrap..."
        /cevac/scripts/log_error.sh "$error"
        exit 1
      fi
    elif [ "$choice" == "2" ]; then
      continue
    fi

  fi
fi
# exit 1
###
# Phase 1: Drop caches
###
/cevac/scripts/seperator.sh
echo "Phase 1: Delete everything"
exclude=""
[ "$isCustom" == "1" ] && exclude="HIST"
# Delete everything
if ! /cevac/scripts/delete.sh -b "$BuildingSName" -m "$Metric" -e "$exclude" -y ; then
  error="Error: could not delete $BuildingSName""_$Metric tables. Aborting bootstrap..."
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

###
# Phase 2: Create CEVAC tables system
###
/cevac/scripts/seperator.sh
echo "Phase: 2 create new views"
if ! /cevac/scripts/CREATE_ALL_VIEWS.sh "$BuildingSName" "$Metric" "$keys_list" "$unitOfMeasureID" ; then
  error="Failed to create views. Aborting bootstrap"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

echo "CHECKPOINT 1"
/cevac/scripts/exec_sql.sh "CHECKPOINT"

###
# Phase 3: Init _CACHE
###
if [ "$autoCACHE" == "true" ]; then
  /cevac/scripts/seperator.sh
  echo "Phase 3: init _CACHE"
  time if ! /cevac/scripts/exec_sql.sh "EXEC CEVAC_CACHE_INIT @tables = '$HIST_VIEW'; EXEC CEVAC_CACHE_INIT @tables = '$DAY_VIEW'" ; then
    error="CEVAC_CACHE_INIT failed. Aborting bootstrap"
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi
fi
echo "CHECKPOINT 2"
/cevac/scripts/exec_sql.sh "CHECKPOINT"

if [ "$customLASR" == "1" ]; then # customLASR is true, upload HIST_LASR instead
  echo "Creating $HIST_LASR"
  if ! /cevac/scripts/CREATE_VIEW.sh "$BuildingSName" "$Metric" "HIST_LASR"; then
    error="Error: Failed to create $HIST_LASR"
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi

  /cevac/scripts/seperator.sh
  echo "Phase 4: create CSVs and rsync to LASR"
  time if ! /cevac/scripts/lasr_append.sh "$BuildingSName" "$Metric" HIST_LASR norun reset ; then
    error="Error uploading $HIST_LASR. Aborting bootstrap."
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi

else # customLASR is false, therefore upload standard HIST
  if [ "$autoLASR" == "true" ]; then
    /cevac/scripts/seperator.sh
    echo "Phase 4: create CSVs and rsync to LASR"
    time if ! /cevac/scripts/lasr_append.sh "$BuildingSName" "$Metric" HIST norun reset ; then
      error="Error uploading $HIST. Aborting bootstrap."
      /cevac/scripts/log_error.sh "$error"
      exit 1
    fi
  fi
fi

echo "CHECKPOINT 3"
/cevac/scripts/exec_sql.sh "CHECKPOINT"
if [ "$autoLASR" == "true" ]; then
  time if ! /cevac/scripts/lasr_append.sh "$BuildingSName" "$Metric" LATEST norun reset ; then
    error="Error uploading $LATEST. Aborting bootstrap."
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi
  if [ "$checkXREF" == "XREF" ]; then
    time if ! /cevac/scripts/lasr_append.sh "$BuildingSName" "$Metric" XREF norun reset ; then
      error="Error uploading $XREF. Aborting bootstrap."
      /cevac/scripts/log_error.sh "$error"
      exit 1
    fi
  fi
fi
[ "$autoCACHE" != "true" ] && /cevac/scripts/toggle_CEVAC_TABLES.sh -b "$BuildingSName" -m "$Metric" -c "autoCACHE" -v "0"
[ "$autoLASR" != "true" ] && /cevac/scripts/toggle_CEVAC_TABLES.sh -b "$BuildingSName" -m "$Metric" -c "autoLASR" -v "0"
/cevac/scripts/unlock.sh

