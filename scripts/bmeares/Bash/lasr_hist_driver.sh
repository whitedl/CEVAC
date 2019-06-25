#! /bin/bash

/home/bmeares/scripts/append_tables.sh

/home/bmeares/scripts/lasr.sh ALL ALERTS HIST
/home/bmeares/scripts/lasr.sh ASC TEMP HIST
/home/bmeares/scripts/lasr.sh ASC IAQ HIST

/home/bmeares/scripts/lasr.sh COOPER TEMP HIST
/home/bmeares/scripts/lasr.sh COOPER POWER HIST

/home/bmeares/scripts/lasr.sh LEE_III TEMP HIST

/home/bmeares/scripts/lasr.sh WATT IAQ HIST
/home/bmeares/scripts/lasr.sh WATT POWER HIST
/home/bmeares/scripts/lasr.sh WATT POWER_SUMS HIST
/home/bmeares/scripts/lasr.sh WATT TEMP HIST
/home/bmeares/scripts/lasr.sh WATT WAP HIST
/home/bmeares/scripts/lasr.sh WATT WAP_DAILY HIST
/home/bmeares/scripts/lasr.sh WATT WAP_FLOOR HIST




