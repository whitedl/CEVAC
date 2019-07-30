#! /bin/bash

Metric="$1"

if [ -z "$1" ]; then
  echo "Usage: $0 [Metric]"
  echo $'Enter the following information.\n'
  echo $'Metric   (e.g. TEMP): '; read Metric
fi

query="EXEC CEVAC_ALL_LATEST @Metric = '$Metric'"

if ! /cevac/scripts/exec_sql.sh "$query" ; then
  error="Could not create CEVAC_ALL_$Metric""_LATEST_HIST"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

