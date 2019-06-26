#! /bin/bash

runsas="norun"
reset="append"

if [ ! -z "$1" ]; then
  runsas="$1"
fi
if [ ! -z "$2" ]; then
  reset="$2"
fi

if [ "$reset" == "reset" ]; then
  echo "Note: Reset detected. Loading entire HIST CSVs caches into LASR"
  echo "If you wish to rebuild CSV cache, delete everything in /srv/csv/"
  echo "If you wish to rebuild SQL cache, run ./init_tables.sh"
fi
if [ "$runsas" == "runsas" ]; then
  echo "Note: runsas detected. Every table will trigger runsas.sh."
  echo "This may harm performance. Omit or use norun for argument 2 to only upload to LASR"
fi


time /home/bmeares/scripts/append_tables.sh

time /home/bmeares/scripts/lasr_append.sh ALL ALERTS HIST UTCDateTime AlertMessage $runsas $reset
time /home/bmeares/scripts/lasr_append.sh ASC TEMP HIST UTCDateTime Alias $runsas $reset
time /home/bmeares/scripts/lasr_append.sh ASC IAQ HIST UTCDateTime Alias $runsas $reset

time /home/bmeares/scripts/lasr_append.sh COOPER TEMP HIST UTCDateTime PointSliceID $runsas $reset
time /home/bmeares/scripts/lasr_append.sh COOPER POWER HIST UTCDateTime PointSliceID $runsas $reset

time /home/bmeares/scripts/lasr_append.sh LEE_III TEMP HIST UTCDateTime Alias $runsas $reset

time /home/bmeares/scripts/lasr_append.sh WATT IAQ HIST UTCDateTime Alias $runsas $reset
time /home/bmeares/scripts/lasr_append.sh WATT POWER HIST UTCDateTime Alias $runsas $reset
time /home/bmeares/scripts/lasr_append.sh WATT POWER_SUMS HIST UTCDateTime Total_Usage $runsas $reset
time /home/bmeares/scripts/lasr_append.sh WATT TEMP HIST UTCDateTime Alias $runsas $reset
time /home/bmeares/scripts/lasr_append.sh WATT WAP HIST "time" Alias $runsas $reset
time /home/bmeares/scripts/lasr_append.sh WATT WAP_DAILY HIST UTCDateTime UTCDateTime $runsas $reset
time /home/bmeares/scripts/lasr_append.sh WATT WAP_FLOOR HIST UTCDateTime UTCDateTime $runsas $reset

echo "All _HIST tables have been loaded. Executing runsas.sh..."
time /home/bmeares/scripts/runsas.sh


