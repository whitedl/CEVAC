#! /bin/bash
if [ -z "$1" ] || [ -z "$2" ]; then
  echo Please enter building, metric, age.
  echo Example. ./lasr.sh WATT TEMP LATEST
fi
building="$1"
metric="$2"
age="$3"
echo Creating CSV: /srv/csv/CEVAC_"$building"_"$metric"_"$age".csv

/home/bmeares/scripts/table_to_csv.sh CEVAC_"$building"_"$metric"_"$age"

echo Uploading CSV to LASR Autoloader...
/home/bmeares/scripts/lasr_upload.sh CEVAC_"$building"_"$metric"_"$age"

echo Finished uploading. Please wait 15 minutes for the data to appear in LASR.

