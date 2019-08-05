#! /bin/sh

# /cevac/scripts/lock.sh

if ! /cevac/scripts/is_unlocked.sh ; then
  echo "is locked"
else
  echo "is unlocked"
fi

/cevac/scripts/unlock.sh
