#! /bin/sh

building=$1
metric=$2
keys_list=$3
if [ -z $4 ]; then unitOfMeasureID="NULL"; else unitOfMeasureID=$4; fi

if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]; then
  echo $'Enter the following information.\n'
  echo $'Building (e.g. WATT): '; read building
  echo $'Metric   (e.g. TEMP): '; read metric
  echo $'Keywords (e.g. SLAB,ZN-T,CRAC)\n     (empty to omit): '; read keys_list
  echo $'UnitOfMeasureID\n     (empty to omit): '; read unitOfMeasureID
fi

if [ -z $building ] || [ -z $metric ]; then
  echo Error!
  exit 1
fi
[ -z $unitOfMeasureID ] && unitOfMeasureID="NULL";
[ -z $keys_list ] && keys_list="NULL";


./CREATE_VIEW.sh $building $metric PXREF $keys_list $unitOfMeasureID
./CREATE_VIEW.sh $building $metric HIST $keys_list $unitOfMeasureID
./CREATE_VIEW.sh $building $metric DAY $keys_list $unitOfMeasureID
./CREATE_VIEW.sh $building $metric LATEST $keys_list $unitOfMeasureID
./CREATE_VIEW.sh $building $metric LATEST_FULL $keys_list $unitOfMeasureID
./CREATE_VIEW.sh $building $metric LATEST_BROKEN $keys_list $unitOfMeasureID
./CREATE_VIEW.sh $building $metric OLDEST $keys_list $unitOfMeasureID

