#! /bin/bash

/home/bmeares/scripts/seperator.sh
echo Appending tables...
tables="CEVAC_WATT_TEMP_HIST_VIEW,"
tables=$tables"CEVAC_WATT_POWER_HIST_VIEW,"
tables=$tables"CEVAC_WATT_IAQ_HIST_VIEW,"
tables=$tables"CEVAC_WATT_POWER_SUMS_HIST_VIEW,"
tables=$tables"CEVAC_ASC_IAQ_HIST_VIEW,"
tables=$tables"CEVAC_ASC_TEMP_HIST_VIEW,"
tables=$tables"CEVAC_LEE_III_TEMP_HIST_VIEW"


/home/bmeares/scripts/exec_sql.sh "EXEC CEVAC_CACHE_APPEND @tables = '$tables'"

echo Finished
