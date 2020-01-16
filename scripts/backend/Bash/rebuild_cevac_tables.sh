#! /bin/sh

# query="SELECT TABLE_NAME 
  # FROM [WFIC-CEVAC].INFORMATION_SCHEMA.TABLES 
  # WHERE TABLE_NAME LIKE 'CEVAC_%HIST_VIEW'
  # ORDER BY TABLE_NAME
# "

# /cevac/scripts/exec_sql.sh "$query" "all_tables.csv"
# sed -i '1d' /cevac/cache/hist_views.csv
readarray tables_array < /cevac/cache/hist_views.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  [ -z "$t" ] && continue
  t=`echo "$t" | sed 's/,/\n/g'`
  B=`echo "$t" | sed '1!d'`
  M=`echo "$t" | sed '2!d'`
  A=`echo "$t" | sed '3!d'`
  echo "$B""_$M"
  read skip
  if [ "$skip" != "" ]; then
    continue
  fi

  # /cevac/scripts/CREATE_ALL_VIEWS.sh "$B" "$A"
  /cevac/scripts/bootstrap.sh -b "$B" -m "$M" -p

done
