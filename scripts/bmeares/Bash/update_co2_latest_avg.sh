#! /bin/sh
# This script queries the latest IAQ reading
/home/bmeares/scripts/seperator.sh

if [ -z $1 ]; then
  echo Error: Please specify a building
  exit 1
fi

building=$1
h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

echo Updating latest air quality for $building...
avg_query="
  SET NOCOUNT ON
  SELECT AVG(ActualValue) AS AVG
    FROM CEVAC_WATT_IAQ_LATEST AS LATEST
    INNER JOIN CEVAC_"$building"_IAQ_XREF AS XREF
      ON XREF.Alias = LATEST.Alias
      WHERE ReadingType = 'CO2'
  "

printf "\nExecuting query:\n $avg_query\n"

# output=$(sqlcmd -S 130.127.218.11 -U wficcm -d WFIC-CEVAC -P 5wattcevacmaint$ -Q "$sum_query")
raw=$(/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$avg_query")
echo Raw data is $raw

# output=$(/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$avg_query" | sed -n '2!p' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?')
output=$(echo $raw | sed -n '2!p' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?')

printf "\nOutput is:"
echo $output
printf "\nUploading to CEVAC_STATS..."

update_query="
SET NOCOUNT ON
UPDATE CEVAC_STATS
SET co2_latest_avg='$output', update_time=GETDATE()
WHERE building = '$building'
";

/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$update_query"
printf "\nFinished\n"
