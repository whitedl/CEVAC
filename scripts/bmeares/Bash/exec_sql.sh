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

if [ ! -z "$2" ]; then
  output="$2"
  echo "Outputting to /home/bmeares/cache/$output"
  if [[ "$query" != *"NOCOUNT"*  ]]; then
    query="
    SET NOCOUNT ON
    $query
    "
  fi
  echo $'Executing query:\n\n'"$query"
  # Get columns and data
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -o "/home/bmeares/cache/temp_$output" -s"," -w 700
  # remove separator
  cat /home/bmeares/cache/temp_$output | sed 2d > /home/bmeares/cache/$output && rm -f /home/bmeares/cache/temp_$output
else
  echo $'Executing query:\n\n'"$query"
  /opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query" -W -w 700
fi


