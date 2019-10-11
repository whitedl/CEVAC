#! /bin/bash

echo "about to do a difficult task"
if ! { /cevac/scripts/test1.sh & } ; then
  echo "Error!!"
fi
wait
echo "done sleeping"
