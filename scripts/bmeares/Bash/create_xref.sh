#! /bin/sh
# This script queries the latest average temperature
if [ -z $1 ]; then
  echo Error: no csv given
  exit 1
fi

create_query=$(csvsql -i mssql $1 | sed -n '2!p')


printf "\nExecuting query:\n $create_query\n"

output=$(sqlcmd -S $h -U $u -d $db -P $p -Q "$sum_query" | sed -n '2!p' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?')




# output=$(sqlcmd -S 130.127.218.11 -U wficcm -d WFIC-CEVAC -P 5wattcevacmaint$ -Q "$sum_query")
# output=$(sqlcmd -S $h -U $u -d $db -P $p -Q "$create_query")

printf "\nOutput is:"
echo $output

printf "\nFinished\n"
