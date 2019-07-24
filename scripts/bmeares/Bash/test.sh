#! /bin/bash

table_CSV="CEVAC_WATT_CO2_HIST_CSV"
t=`/cevac/scripts/sql_value.sh "IF OBJECT_ID('$table_CSV') IS NOT NULL SELECT 'EXISTS' ELSE SELECT 'DNE'"`
echo $t
if [ "$t" == "EXISTS" ]; then
  echo "exists";
elif [ "$t" == "DNE" ]; then
  echo "dne";
else
  echo "huh";
fi

