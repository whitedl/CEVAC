#! /bin/bash

PARENT_COMMAND=$(ps -o comm= $PPID)

if ! /cevac/scripts/is_unlocked.sh "$PARENT_COMMAND" ; then
  error="$PARENT_COMMAND is currently running"
  /cevac/scripts/log_error.sh "$error"
fi


