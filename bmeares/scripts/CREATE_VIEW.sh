#! /bin/sh
# ./seperator.sh
building=$1
metric=$2
age=$3
keys_list=$4
if [ -z $5 ]; then unitOfMeasureID="NULL"; else unitOfMeasureID=$5; fi

if [ -z $1 ] || [ -z $2 ] || [ -z $3 ] || [ -z $4 ]; then
  echo $'Enter the following information.\n'
  echo $'Building (e.g. WATT): '; read building
  echo $'Metric   (e.g. TEMP): '; read metric
  echo $'Age      (e.g. HIST): '; read age
  echo $'Keywords (e.g. SLAB,ZN-T,CRAC)\n     (empty to omit): '; read keys_list
  echo $'UnitOfMeasureID\n     (empty to omit): '; read unitOfMeasureID
fi


if [ -z $building ] || [ -z $metric ] || [ -z $age ]; then
  echo Error!
  exit 1
fi
if [ -z $unitOfMeasureID ] || [ "$unitOfMeasureID" = "NULL" ]; then
  unitOfMeasureID="NULL"; fi
if [ -z $keys_list ] || [ "$keys_list" = "NULL" ]; then keys_list=""; fi

building="'"$building"'"
metric="'"$metric"'"
age="'"$age"'"
keys_list="'"$keys_list"'"


h='130.127.218.11'
u='wficcm'
db='WFIC-CEVAC'
p='5wattcevacmaint$'

query="
SET NOCOUNT ON
EXEC CEVAC_VIEW @Building = $building, @Metric = $metric, @Age = $age, @keys_list = $keys_list, @unitOfMeasureID = $unitOfMeasureID
"

echo -e "Executing query:\n$query"

/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -Q "$query"\
  && echo Created CEVAC_"$building"_"$metric"_"$age"\
  || echo Error! Views could not be created.


