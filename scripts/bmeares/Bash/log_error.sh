#! /bin/sh

PARENT_COMMAND=$(ps -o comm= $PPID)
ErrorMessage="$1"
ProcessName="$PARENT_COMMAND"

if [ -z "$1" ] ; then
  echo "Usage: $0 [ErrorMessage] {TableName}"
  exit 1
fi

if [ -z "$2" ]; then
  TableName="NULL"
else
  TableName="'$TableName'"
fi

sql="
INSERT INTO CEVAC_ERRORS(TableName, ErrorMessage, UTCDateTime, ProcessName)
VALUES (
  $TableName,
  '$ErrorMessage',
  GETUTCDATE(),
  '$ProcessName'
)
"

/cevac/scripts/exec_sql.sh "$sql"
message="
Error  : $ProcessName Failed.
Message: $ErrorMessage
Event logged in CEVAC_ERRORS
"
echo "$message"
