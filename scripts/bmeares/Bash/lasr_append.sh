#! /bin/bash
if [ -z "$1" ] || [ -z "$2" ]; then
  echo Please enter building, metric, age.
  echo Example. ./lasr_append.sh WATT TEMP LATEST
  exit 1
fi
building="$1"
metric="$2"
age="$3"
echo Creating CEVAC_"$building"_"$metric"_"$age".csv

/home/bmeares/scripts/table_to_csv_append.sh CEVAC_"$building"_"$metric"_"$age"

echo Uploading CSV to LASR Autoloader...
/home/bmeares/scripts/lasr_upload_append.sh CEVAC_"$building"_"$metric"_"$age"

echo Finished uploading to LASR

