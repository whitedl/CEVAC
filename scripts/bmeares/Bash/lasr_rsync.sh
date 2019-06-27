#! /bin/sh

if [ -z "$1" ]; then
  echo "Error: Missing table name"
  exit 1
fi
table="$1"
rsync -vh --progress /srv/csv/$table.csv wfic-sas-im-hd.clemson.edu:/opt/sasinside/sasconfig/Lev1/AppData/SASVisualAnalytics/VisualAnalyticsAdministrator/AutoLoad

