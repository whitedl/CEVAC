#! /bin/sh
# ./seperator.sh

building=$1
metric=$2
age=$3
keys_list=$4


query=$(cat demo.txt)
echo "$query" | sed "s/#BUILDING#/$building/1"
# filtered=$(sed "s/#BUILDING#/$building/1" $query)
# filtered=$(sed "s/#METRIC#/$metric/1" $filtered)
# filtered=$(sed "s/#AGE#/$age/1" $filtered)
# filtered=$(sed "s/#KEYS_LIST#/$keys_list/1" $filtered)

# echo "$filtered"


