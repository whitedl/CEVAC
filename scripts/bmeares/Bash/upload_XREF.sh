#! /bin/bash
! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

fname="$1"
[ -z "$fname" ] && /cevac/scripts/unlock.sh  && exit 1

python3 -V
# if ! python3 /cevac/python/csv_process.py "$fname" ; then
  # /cevac/scripts/log_error.sh "Failed to upload XREF"
  # exit 1
# fi

/cevac/scripts/unlock.sh
