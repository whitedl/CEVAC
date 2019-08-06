#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

echo "Updating HIST"
if ! /cevac/scripts/lasr_hist_driver.sh ; then
  /cevac/scripts/log_error.sh "Failed updating HIST tables"
  exit 1
fi
echo "Updating LATEST"
if ! /cevac/scripts/lasr_latest_driver.sh ; then
  /cevac/scripts/log_error.sh "Failed updating LATEST tables"
  exit 1
fi
echo "Updating STATS"
if ! /cevac/scripts/UPDATE_STATS.sh ; then
  /cevac/scripts/log_error.sh "Failed updating stats"
  exit 1
fi

/cevac/scripts/unlock.sh
