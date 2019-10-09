#! /bin/bash

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh
usage="Usage:
  -b BuildingSName
  -d BuildingDName
  -k BuildingKey

  -h help
  -y run without asking
"
while getopts b:d:k:hy option; do
  case "${option}"
    in
    h) echo "$usage" && /cevac/scripts/unlock.sh && exit 1 ;;
    b) BuildingSName=${OPTARG};;
    d) BuildingDName=${OPTARG};;
    k) BuildingKey=${OPTARG};;
    y) yes="yes";;
  esac
done

[ -z "$BuildingDName" ] && echo "$usage" && /cevac/scripts/unlock.sh && exit 1
[ -z "$BuildingSName" ] && echo "$usage" && /cevac/scripts/unlock.sh && exit 1
[ -z "$BuildingKey" ] && echo "$usage" && /cevac/scripts/unlock.sh && exit 1

sql="
DELETE FROM CEVAC_BUILDING_INFO WHERE BuildingSName = '$BuildingSName';
INSERT INTO CEVAC_BUILDING_INFO(BuildingSName, BuildingDName, BuildingKey)
VALUES(
  '$BuildingSName',
  '$BuildingDName',
  '$BuildingKey'
)
"
if ! /cevac/scripts/exec_sql.sh "$sql" ; then
  /cevac/scripts/log_error.sh
fi

/cevac/scripts/unlock.sh
