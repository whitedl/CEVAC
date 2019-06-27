#! /bin/sh
# This script queries the latest average power use
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

echo Updating latest power sum for $building...
sum_query="
  SET NOCOUNT ON
  SELECT SUM(ActualValue) AS SUM
  FROM CEVAC_"$building"_POWER_LATEST"

printf "\nExecuting query:\n $sum_query\n"

# output=$(sqlcmd -S 130.127.218.11 -U wficcm -d WFIC-CEVAC -P 5wattcevacmaint$ -Q "$sum_query")
raw=$(/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$sum_query")
echo Raw data is: $raw

output=$(echo $raw | sed -n '2!p' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?')

printf "\nOutput is:"
echo $output
printf "\nUploading to CEVAC_STATS..."

update_query="
SET NOCOUNT ON
UPDATE CEVAC_STATS
SET power_latest_sum='$output', update_time=GETDATE()
WHERE building = '$building'
";

/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$update_query"
printf "\nFinished\n"
