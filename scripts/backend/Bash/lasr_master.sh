#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

echo "Updating HIST"
if ! /cevac/scripts/lasr_driver.sh -a "HIST"; then
  /cevac/scripts/log_error.sh "Failed updating HIST tables"
  exit 1
fi

echo "Updating LATEST"
if ! /cevac/scripts/lasr_driver.sh -a "LATEST"; then
  /cevac/scripts/log_error.sh "Failed updating LATEST tables"
  exit 1
fi
echo "Updating STATS"
if ! /cevac/scripts/UPDATE_STATS.sh ; then
  /cevac/scripts/log_error.sh "Failed updating stats"
  exit 1
fi
/cevac/scripts/exec_sql.sh "CHECKPOINT"
/cevac/scripts/unlock.sh
