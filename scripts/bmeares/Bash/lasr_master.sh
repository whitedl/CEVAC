#! /bin/bash

echo "Updating HIST"
/cevac/scripts/lasr_hist_driver.sh
echo "Updating LATEST"
/cevac/scripts/lasr_latest_driver.sh
echo "Updating STATS"
/cevac/scripts/UPDATE_STATS.sh
