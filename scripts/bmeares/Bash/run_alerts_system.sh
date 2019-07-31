#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

sudo python3 /cevac/python/alerts/alert_system.py

/cevac/scripts/unlock.sh
