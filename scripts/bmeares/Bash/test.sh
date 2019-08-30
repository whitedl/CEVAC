#! /bin/bash

while getopts i:t: option; do
  case "${option}"
    in
    i) I=${OPTARG};;
    t) T=${OPTARG};;
  esac
done

echo "I is $I"
echo "T is $T"
