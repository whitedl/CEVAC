#! /bin/bash

PARENT_COMMAND=$(ps -o comm= $PPID)
[ ! -z "$1" ] && PARENT_COMMAND="$1"

lock_file="/tmp/"`echo "$PARENT_COMMAND" | sed 's/[^a-z  A-Z]//g'`".lock"
if [ -f "$lock_file" ]; then
  exit 1
fi
