#! /bin/sh
building="$1"
metric="$2"
age="$3"
keys_list="$4"
if [ -z "$5" ]; then unitOfMeasureID="NULL"; else unitOfMeasureID="$5"; fi

if [ -z $1 ] || [ -z $2 ]; then
  echo "Usage: $0 [BuildingSName] [Metric] [Age] {Keywords} {UnitOfMeasureID}"
  echo $'Enter the following information.\n'
  echo $'Building (e.g. WATT): '; read building
  echo $'Metric   (e.g. TEMP): '; read metric
  echo $'Age      (e.g. HIST): '; read age
  echo $'Keywords (e.g. SLAB,ZN-T,CRAC)\n     (empty to omit): '; read keys_list
  echo $'UnitOfMeasureID\n     (empty to omit): '; read unitOfMeasureID
fi

if [ -z "$building" ] || [ -z "$metric" ] || [ -z "$age" ]; then
  echo "Error! Run again with all fields entered correctly."
  exit 1
fi
if [ -z "$unitOfMeasureID" ] || [ "$unitOfMeasureID" = "NULL" ]; then
  unitOfMeasureID="NULL"; fi
if [ -z "$keys_list" ] || [ "$keys_list" = "NULL" ]; then keys_list=""; fi

query="EXEC CEVAC_VIEW @Building = '$building', @Metric = '$metric', @Age = '$age', @keys_list = '$keys_list', @unitOfMeasureID = $unitOfMeasureID"

if ! /cevac/scripts/exec_sql.sh "$query" ; then
  error="Could not create $building""_$metric""_$age"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

