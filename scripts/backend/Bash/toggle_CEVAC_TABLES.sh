#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

while getopts b:m:c:t:v:h option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    c) column=${OPTARG};;
    t) TableName=${OPTARG};;
    v) value=${OPTARG};;
    h) h=${OPTARG};;
  esac
done
usage="Usage:
  -b BuildingSName
  -m Metric
  -t TableName
  -c column
  -v value
  -h help
  "
HIST="CEVAC_$BuildingSName""_$Metric""_HIST"
HIST_LASR="CEVAC_$BuildingSName""_$Metric""_HIST_LASR"
LATEST="CEVAC_$BuildingSName""_$Metric""_LATEST"
HIST_VIEW="CEVAC_$BuildingSName""_$Metric""_HIST_VIEW"
if [ ! -z "$h" ]; then
    echo "$usage"
    /cevac/scripts/unlock.sh
  exit 0
fi

if [ -z "$column" ] || [ -z "$value" ]; then
  echo "$usage"
  /cevac/scripts/unlock.sh
  exit 1
fi
if [ ! -z "$TableName" ]; then
  query="
  UPDATE CEVAC_TABLES
  SET $column = '$value'
  WHERE TableName = '$TableName'
  "
elif [ ! -z "$BuildingSName" ] && [ ! -z "$Metric" ]; then
  if [ "$column" == "autoCACHE" ]; then
    query="
    UPDATE CEVAC_TABLES
    SET $column = '$value'
    WHERE TableName = '$HIST_VIEW'
    "
  elif [ "$column" == "autoLASR" ]; then
    query="
    UPDATE CEVAC_TABLES
    SET $column = '$value'
    WHERE TableName = '$HIST' OR TableName = '$LATEST' OR TableName = '$HIST_LASR'
    "
  fi
  
fi

/cevac/scripts/exec_sql.sh "$query"

/cevac/scripts/unlock.sh
