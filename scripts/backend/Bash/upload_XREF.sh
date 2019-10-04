#! /bin/bash
! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

fname="$1"
[ -z "$fname" ] && /cevac/scripts/unlock.sh  && exit 1

# python3 -V
echo "Calling python script..."
/cevac/scripts/log_activity.sh -p $PARENT_COMMAND -t "$fname"
out=`/usr/bin/python3 /cevac/python/csv_process.py "$fname" 2>&1`
echo "$out"
# if ! python3 /cevac/python/csv_process.py "$fname" ; then
  # /cevac/scripts/log_error.sh "Failed to upload XREF"
  # exit 1
# fi

/cevac/scripts/unlock.sh
