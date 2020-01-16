#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

sudo python3 /cevac/python/alert_system.py

/cevac/scripts/unlock.sh
