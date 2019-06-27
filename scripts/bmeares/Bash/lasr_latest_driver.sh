#! /bin/bash
runsas="runsas"
reset="reset"

if [ ! -z "$1" ]; then
  runsas="$1"
fi
if [ ! -z "$2" ]; then
  reset="$2"
fi

if [ "$reset" == "reset" ]; then
  echo "Note: Reset detected. Loading entire LATEST CSVs caches into LASR"
fi
if [ "$runsas" == "runsas" ]; then
  echo "Note: runsas detected. Every table will trigger runsas.sh."
fi


/home/bmeares/scripts/append_tables.sh

# /home/bmeares/scripts/lasr.sh ALL ALERTS HIST
# /home/bmeares/scripts/lasr.sh WATT WAP HIST


# /home/bmeares/scripts/lasr.sh ASC IAQ LATEST
time /home/bmeares/scripts/lasr.sh ASC TEMP LATEST UTCDateTime Alias $runsas $reset

/home/bmeares/scripts/lasr.sh COOPER TEMP LATEST UTCDateTime Alias $runsas $reset
# /home/bmeares/scripts/lasr.sh COOPER POWER LATEST UTCDateTime Alias $runsas $reset

/home/bmeares/scripts/lasr.sh LEE_III TEMP LATEST UTCDateTime Alias $runsas $reset

/home/bmeares/scripts/lasr.sh WATT IAQ LATEST UTCDateTime Alias $runsas $reset
/home/bmeares/scripts/lasr.sh WATT POWER LATEST UTCDateTime Alias $runsas $reset
/home/bmeares/scripts/lasr.sh WATT TEMP LATEST UTCDateTime Alias $runsas $reset

echo "All _LATEST tables have been loaded. Executing runsas.sh..."
time /home/bmeares/scripts/runsas.sh


