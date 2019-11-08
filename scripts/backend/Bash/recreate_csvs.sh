#! /bin/bash
error=""
# echo "Warning: This will delete everything in /srv/csv/ and will take some time to recreate."
echo "Continue? (y/N)"
read choice
if [ "$choice" != "y" ] && [ "$choice" != "Y" ]; then
  echo "Quitting..."
  exit 1
fi

# echo "Deleting everything in /srv/csv/"
# rm -f /srv/csv/*

csv_tables_query="
SELECT RTRIM(BuildingSName), RTRIM(Metric), RTRIM(Age) FROM CEVAC_TABLES
WHERE autoLASR = 1
AND Age = 'HIST'
"
if ! /cevac/scripts/exec_sql.sh "$csv_tables_query" "csv_tables.csv" ; then
  error="Failed to get CSV tables"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

# Remove header from csv
sed -i '1d' /cevac/cache/csv_tables.csv
readarray tables_array < /cevac/cache/csv_tables.csv

# echo "Dropping all _CSV tables..."
for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  if [ -z "$t" ]; then
    continue
  fi
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`

  table="CEVAC_$B""_$M""_$A"
  table_csv="CEVAC_$B""_$M""_$A""_CSV"
  rm -f /srv/csv/$table.csv
  echo $table_csv
 
  if ! /cevac/scripts/exec_sql.sh "IF OBJECT_ID('$table_csv') IS NOT NULL DROP TABLE $table_csv" ; then
    error="Error dropping $table_csv"
    /cevac/scripts/log_error.sh "$error" "CEVAC_$B""_$M""_$A"
    exit 1
  fi

  echo "Recreating and uploading $table_csv"
  time if ! /cevac/scripts/lasr_append.sh $B $M $A "norun" "reset" ; then
    error="Failed lasr_append for $B""_$M""_$A"
    /cevac/scripts/log_error.sh "$error" "CEVAC_$B""_$M""_$A"
    exit 1
  fi

done


