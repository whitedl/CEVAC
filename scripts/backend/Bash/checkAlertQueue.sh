#! /bin/sh

! /cevac/scripts/check_lock.sh -e "false" && exit 0
/cevac/scripts/lock.sh

working_dir=/home/hchall/Documents/cevac/hcevac/alerts/alert_system2/

# /cevac/CEVAC/alerts/alert_system2/main.py
cd "$working_dir"
python3 main.py -q -a -v -s --log false
touch ~/harrison.txt
/cevac/scripts/unlock.sh
