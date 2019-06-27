#! /bin/bash

if [ -z "$1" ]; then
  echo Error: Missing table name
  exit 1
fi
table="$1"
echo Sending newest lines of $table.csv over rsync...
rsync -v /home/bmeares/cache/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad/Append

if [ "$2" == "norun"]; then
  echo "norun selected. Skipping runsas and exiting."
  exit 1
fi

echo Running LASR script...
./runsas.sh

echo Done! $table has been loaded into LASR
