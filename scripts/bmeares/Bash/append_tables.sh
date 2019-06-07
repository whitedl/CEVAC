#! /bin/bash

/home/bmeares/scripts/seperator.sh
echo Appending tables...
tables="CEVAC_WATT_TEMP_HIST,CEVAC_WATT_POWER_HIST,CEVAC_WATT_IAQ_HIST"


/home/bmeares/scripts/exec_sql.sh "EXEC CEVAC_CACHE_APPEND @tables = '$tables'"

echo Finished
