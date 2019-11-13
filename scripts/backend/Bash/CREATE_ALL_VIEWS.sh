#! /bin/sh
error=""
building="$1"
metric="$2"
keys_list="$3"
HIST_VIEW="CEVAC_$building""_$metric""_HIST_VIEW"
HIST_LASR="CEVAC_$building""_$metric""_HIST_LASR"
if [ -z "$4" ]; then unitOfMeasureID="NULL"; else unitOfMeasureID="$4"; fi

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 [BuildingSName] [Metric] {keys_list} {unitOfMeasureID}"
  echo $'Enter the following information.\n'
  echo $'Building (e.g. WATT): '; read building
  echo $'Metric   (e.g. TEMP): '; read metric
fi
isCustom=`/cevac/scripts/sql_value.sh "SELECT isCustom FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW'"`
checkXREF=`/cevac/scripts/sql_value.sh "EXEC CHECK_XREF @BuildingSName = '$building', @Metric = '$metric'"`
if [ "$checkXREF" != "XREF" ] && [ "$isCustom" != "1" ]; then
  echo "Warning: CEVAC_$building""_$metric""_XREF"" not found."
  uid=`/cevac/scripts/sql_value.sh "SELECT TOP 1 unitOfMeasureID FROM CEVAC_METRIC WHERE Metric = '$metric'"`
  if [ ! -z "$uid" ]; then # new metric
    echo "UnitOfMeasureID: $uid has been defined for Metric: $metric"
    echo "This script will use $uid as the unitOfMeasureID unless specified below."
    echo $'unitOfMeasureID\n     (empty to use '$uid'): '; read unitOfMeasureID
  else
    echo $'unitOfMeasureID\n     (important!): '; read unitOfMeasureID
  fi
  echo $'Keywords (e.g. SLAB,ZN-T,CRAC)\n     (empty to omit): '; read keys_list
fi

if [ -z "$building" ] || [ -z "$metric" ]; then
  echo "Error! Run $0 again with the correct parameters"
  exit 1
fi
[ -z "$unitOfMeasureID" ] && unitOfMeasureID="NULL";
[ -z "$keys_list" ] && keys_list="NULL";

if [ "$isCustom" == "1" ]; then
  ages_array=("HIST" "DAY" "LATEST" "LATEST_FULL" "LATEST_BROKEN" "OLDEST")
else
  ages_array=("PXREF" "HIST" "DAY" "LATEST" "LATEST_FULL" "LATEST_BROKEN" "OLDEST")
fi

if [ "$metric" == "WAP" ]; then
  sql="EXEC CEVAC_WAP @BuildingSName = '$building', @Metric = '$metric'" 
  if ! /cevac/scripts/exec_sql.sh "$sql" ; then
    error="Error encountered when creating $building""_$metric tables"
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi
fi

for a in "${ages_array[@]}"; do
  echo "Creating CEVAC_$building""_$metric""_$a"
  if ! /cevac/scripts/CREATE_VIEW.sh $building $metric $a $keys_list $unitOfMeasureID ; then
    error="Error encountered when creating $building""_$metric""_$a"
    /cevac/scripts/log_error.sh "$error"
    exit 1
  fi
done

