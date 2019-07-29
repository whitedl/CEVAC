#! /bin/sh

h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

PARENT_COMMAND=$(ps -o comm= $PPID)
ErrorMessage="$1"
ProcessName="$PARENT_COMMAND"

if [ -z "$1" ] ; then
  echo "Usage: $0 [ErrorMessage] {TableName}"
  exit 1
fi

sql="
INSERT INTO CEVAC_ERRORS(TableName, ErrorMessage, UTCDateTime, ProcessName)
VALUES (
  '$TableName',
  '$ErrorMessage',
  GETUTCDATE(),
  '$ProcessName'
)
"

/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$sql" -W -b -w 700
message="
Error  : $ProcessName Failed.
Message: $ErrorMessage
Event logged in CEVAC_ERRORS
"
echo "$message"
exit 1
