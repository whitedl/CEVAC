#! /bin/bash

PARENT_COMMAND=$(ps -o comm= $PPID)
ProcessName="$PARENT_COMMAND"
TableName=""
while getopts t:p: option; do
  case "${option}"
    in
    t) TableName=${OPTARG};;
    p) ProcessName=${OPTARG};;
  esac
done

sql="
INSERT INTO CEVAC_ACTIVITY_LOG(TableName, UTCDateTime, ProcessName)
VALUES (
  '$TableName',
  GETUTCDATE(),
  '$ProcessName'
)
"

/cevac/scripts/exec_sql.sh "$sql"
