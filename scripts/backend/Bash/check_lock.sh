#! /bin/bash
reportError="true"
while getopts e: option; do
  case "${option}"
    in
    e) reportError=${OPTARG};;
  esac
done

PARENT_COMMAND=$(ps -o comm= $PPID)

if [ "$reportError" == "true" ]; then
  if ! /cevac/scripts/is_unlocked.sh "$PARENT_COMMAND" ; then
    error="$PARENT_COMMAND is currently running"
    /cevac/scripts/log_error.sh "$error"
  fi
fi

