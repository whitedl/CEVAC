#! /bin/sh

if [ -z "$1" ]; then
  echo Error: Missing SQL script
  exit 1
fi

script=$1
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'


# output=$(sqlcmd -S 130.127.218.11 -U wficcm -d WFIC-CEVAC -P 5wattcevacmaint$ -Q "$sum_query")

echo $'Executing script:\n\n'$script

if ! /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -i "$script" ; then
  error="Could not execute $script"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

