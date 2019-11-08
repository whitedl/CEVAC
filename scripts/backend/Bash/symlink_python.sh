#! /bin/bash

for f in $(find /cevac/CEVAC/ -name *.py); do
  ln -s $f /cevac/python/
  # echo "$f"
done
