#! /bin/bash
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo Please enter building, metric, age.
  echo "Usage: ./lasr_append [BLDG] [METRIC] [AGE] [UTCDateTime] [Alias] [runsas] [reset]"
  exit 1
fi
if [ -z "$4" ]; then
  echo "Error: Missing time metric (e.g. UTCDateTime)"
  echo "Usage: ./lasr_append [BLDG] [METRIC] [AGE] [UTCDateTime] [Alias] [runsas] [reset]"
  exit 1
fi
if [ -z "$5" ]; then
  echo "Error: Missing name metric (e.g. Alias)"
  echo "Usage: ./lasr_append [BLDG] [METRIC] [AGE] [UTCDateTime] [Alias] [runsas] [reset]"
  exit 1
fi
if [ "$6" == "runsas" ]; then
  runsas="true"
fi
if [ "$7" == "reset" ]; then
  reset="true"
fi



UTCDateTime="$4"
Alias="$5"

building="$1"
metric="$2"
age="$3"
table=CEVAC_"$building"_"$metric"_"$age"

echo Creating $table.csv

/home/bmeares/scripts/table_to_csv_append.sh $table $UTCDateTime $Alias

echo Uploading CSV to LASR Autoloader...
# /home/bmeares/scripts/lasr_upload_append.sh CEVAC_"$building"_"$metric"_"$age" $UTCDateTime $Alias

if [ "$reset" == "true" ]; then
  echo Reset detected. Uploading entire $table.csv
  rsync -vh --progress /srv/csv/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad
else
  echo Sending newest lines of $table.csv over rsync...
  rsync -vh --progress /home/bmeares/cache/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad/Append
fi


if [ "$runsas" == "true" ]; then
  echo "runsas detected. Executing LASR Autoload script..."
  ./runsas.sh
  echo Finished uploading to LASR
else
  echo "runsas not detected. $table will be loaded into LASR on the next Autoload schedule"
fi


