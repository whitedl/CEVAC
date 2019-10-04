#! /bin/sh

if [ -z "$1" ]; then
  echo Error: Missing SQL query
  exit 1
fi
query="$1"
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'
query="
SET NOCOUNT ON
$1
"
/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -w 700 -b -h-1


