#! /bin/sh

if [ -z "$1" ]; then
  echo Error: Missing SQL query
  exit 1
fi

query=$1
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'


# output=$(sqlcmd -S 130.127.218.11 -U wficcm -d WFIC-CEVAC -P 5wattcevacmaint$ -Q "$sum_query")

echo $'Executing query:\n\n'"$query"

raw=$(/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query")
echo "$raw"

