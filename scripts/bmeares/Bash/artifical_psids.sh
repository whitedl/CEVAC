#! /bin/bash

# xref_query="SELECT TableName FROM CEVAC_TABLES WHERE Age = 'XREF' AND TableName NOT LIKE '%CSV%'"
xref_query="
SELECT info.TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS AS info
  INNER JOIN CEVAC_TABLES AS ct ON info.TABLE_NAME = ct.TableName
  WHERE info.COLUMN_NAME = 'PointSliceID'
  AND ct.Age = 'XREF'
  AND ct.TableName NOT LIKE '%CSV%'
"

/cevac/scripts/exec_sql.sh "$xref_query" "xrefs.csv"

sed -i '1d' /cevac/cache/xrefs.csv
readarray tables_array < /cevac/cache/xrefs.csv

for t in "${tables_array[@]}"; do
  t=`echo "$t" | tr -d '\n'`
  [ -z "$t" ] && continue
  echo "$t"
  sql="
  DELETE FROM CEVAC_ARTIFICIAL_PSIDS WHERE TableName = '$t';
  INSERT INTO CEVAC_ARTIFICIAL_PSIDS
    SELECT PointSliceID, Alias, '$t' AS 'TableName'
    FROM $t
    WHERE PointSliceID < 0
  "
  echo "$sql"
  if ! /cevac/scripts/exec_sql.sh "$sql" ; then
    # echo "Error. Aborting append"
    /cevac/scripts/log_error.sh "Error updating artificial psids" "$t"
    exit 1
  fi
done


