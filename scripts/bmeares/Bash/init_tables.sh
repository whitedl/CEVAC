#! /bin/bash

/home/bmeares/scripts/seperator.sh
echo Initializing tables...
tables_array=(
CEVAC_WATT_TEMP_HIST_VIEW
CEVAC_WATT_IAQ_HIST_VIEW
CEVAC_WATT_POWER_HIST_VIEW
CEVAC_WATT_POWER_SUMS_HIST_VIEW
CEVAC_ASC_IAQ_HIST_VIEW
CEVAC_ASC_TEMP_HIST_VIEW
CEVAC_LEE_III_TEMP_HIST_VIEW
)
for t in "${tables_array[@]}"; do
  sql="EXEC CEVAC_CACHE_INIT @tables = '"$t"'"
  /home/bmeares/scripts/exec_sql.sh "$sql"
done


echo Finished
