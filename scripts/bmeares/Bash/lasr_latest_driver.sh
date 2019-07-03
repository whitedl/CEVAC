#! /bin/bash
runsas="norun"
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


time /home/bmeares/scripts/append_tables.sh

# 	time /cevac/scripts/lasr_append.sh ALL ALERTS HIST
# 	time /cevac/scripts/lasr_append.sh WATT WAP HIST


# 	time /cevac/scripts/lasr_append.sh ASC IAQ LATEST
	time /cevac/scripts/lasr_append.sh ASC TEMP LATEST UTCDateTtime Alias $runsas $reset

	time /cevac/scripts/lasr_append.sh COOPER TEMP LATEST UTCDateTtime Alias $runsas $reset
# 	time /cevac/scripts/lasr_append.sh COOPER POWER LATEST UTCDateTtime Alias $runsas $reset

	time /cevac/scripts/lasr_append.sh LEE_III TEMP LATEST UTCDateTtime Alias $runsas $reset

	time /cevac/scripts/lasr_append.sh WATT IAQ LATEST UTCDateTtime Alias $runsas $reset
	time /cevac/scripts/lasr_append.sh WATT POWER LATEST UTCDateTtime Alias $runsas $reset
	time /cevac/scripts/lasr_append.sh WATT TEMP LATEST UTCDateTtime Alias $runsas $reset

if [ "$runsas" == "runsas" ]; then
  echo Running sas...
  time /home/bmeares/scripts/runsas.sh
fi

echo Done with _LATEST
