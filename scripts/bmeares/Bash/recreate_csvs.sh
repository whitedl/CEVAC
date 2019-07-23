#! /bin/bash

echo "Warning: This will delete everything in /srv/csv/ and will take some time to recreate."
echo "Continue? (y/N)"
read choice
if [ "$choice" != "y" ] && [ "$choice" != "Y" ]; then
  echo "Quitting..."
  exit 1
fi

echo "Deleting everything in /srv/csv/"
rm -f /srv/csv/*

csv_tables_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE TableName LIKE '%_CSV%' AND TableName NOT LIKE '%BROKEN%' AND TableName NOT LIKE '%FULL%'
AND customLASR = 0
"
/cevac/scripts/exec_sql.sh "$csv_tables_query" "csv_tables.csv"

# Remove header from csv
sed -i '1d' /cevac/cache/csv_tables.csv
readarray tables_array < /cevac/cache/csv_tables.csv

echo "Dropping all _CSV tables..."
for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  if [ -z "$t" ]; then
    continue
  fi
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`

  table_csv="CEVAC_$B""_$M""_$A""_CSV"
  echo $table_csv
 
  out=`/cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_csv') IS NOT NULL DROP TABLE $table_csv"`
  error=`echo "$out" | grep 'Msg'`
  error2=`echo "$out" | awk '/Msg/ { getline; print $0 }'`

  if [ ! -z "$error" ]; then
    echo "Error dropping $table_csv"
    echo "Error Message:"
    echo "$error"
    echo "$error2"

    echo "Print full output log? (y/N)": 
    read choice
    if [ "$choice" == "y" ] || [ "$choice" == "Y" ]; then
      echo "$out"
    fi
    exit 1
  fi



  echo "Recreating and uploading $table_csv"
  time /cevac/scripts/lasr_append.sh $B $M $A "norun" "reset"

done


