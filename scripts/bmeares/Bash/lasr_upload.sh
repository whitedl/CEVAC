#! /bin/bash

if [ -z "$1" ]; then
  echo Error: Missing table name
  exit 1
fi


table="$1"
remote_command="rsync bmeares@wfic-cevac1:/srv/csv/$table.csv /opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad"
echo Sending $table.csv over rsync...
rsync -v /srv/csv/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad
# ssh sas@wfic-sas-im-hd.clemson.edu "$remote_command"

echo Done. Running LASR script...
runsas="/opt/sasinside/sasconfig/Lev1/Applications/SASVisualAnalytics/VisualAnalyticsAdministrator/runsas.sh"
ssh sas@wfic-sas-im-hd.clemson.edu "$runsas"

echo Done! $table has been loaded into LASR
