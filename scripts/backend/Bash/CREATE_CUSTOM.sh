#! /bin/sh
# ./seperator.sh
BuildingSName="$1"
Metric="$2"
DateTimeName="$3"
IDName="$4"
AliasName="$5"
DataName="$6"
Dependencies="$7"
error=""

echo "Usage: $0 [BuildingSName] [Metric] [DateTimeName] [IDName] [AliasName] [DataName] [Dependencies]"

if [ -z "$1" ]; then
  echo $'BuildingSName       (e.g. WATT): '; read BuildingSName
fi
if [ -z "$2" ]; then
  echo $'Metric              (e.g. TEMP): '; read Metric
fi
HIST_VIEW="CEVAC_$BuildingSName""_$Metric"_"HIST_VIEW"
def_file="/cevac/CUSTOM_DEFS/$HIST_VIEW.sql"
if [ ! -f "$def_file" ]; then
  error="$def_file is missing"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi

if [ -z "$3" ]; then
  echo $'DateTimeName (def. UTCDateTime):'; read DateTimeName
  [ -z "$DateTimeName" ] && DateTimeName="UTCDateTime"
fi
if [ -z "$4" ]; then
  echo $'IDName      (def. PointSliceID):'; read IDName
  [ -z "$IDName" ] && IDName="PointSliceID"
fi
if [ -z "$5" ]; then
  echo $'AliasName          (def. Alias):'; read AliasName
  [ -z "$AliasName" ] && AliaseName="Alias"
fi
if [ -z "$6" ]; then
  echo $'DataName     (def. ActualValue):'; read DataName
  [ -z "$DataName" ] && DataName="ActualValue"
fi
if [ -z "$7" ]; then
  echo $'Dependencies   (comma-separated):'; read Dependencies
fi


CREATE_VIEW="
CREATE VIEW $HIST_VIEW AS
"

Definition=`cat $def_file | sed "s/'/''/g"`
Definition="$CREATE_VIEW $Definition"

# Insert into CEVAC_TABLES
cevac_tables_query="
DELETE FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW';
INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Definition, Dependencies)
  VALUES (
    '$BuildingSName',
    '$Metric',
    'HIST',
    '$HIST_VIEW',
    '$DateTimeName',
    '$IDName',
    '$AliasName',
    '$DataName',
    1,
    '$Definition',
    '$Dependencies'
  )
"
# Reset CEVAC_TABLES
/cevac/scripts/exec_sql.sh "DELETE FROM CEVAC_TABLES WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric'"
echo "$cevac_tables_query" > /cevac/cache/CEVAC_TABLES_$HIST_VIEW.sql
/cevac/scripts/exec_sql_script.sh "/cevac/cache/CEVAC_TABLES_$HIST_VIEW.sql"
echo "Inserted $HIST_VIEW into CEVAC_TABLES"

# Create custom CREATE_HIST_VIEW and execute it
custom_query="
SET NOCOUNT ON;
EXEC CEVAC_CUSTOM_HIST @BuildingSName = '$BuildingSName', @Metric = '$Metric'
;
"
CUSTOM_file="/cevac/cache/CUSTOM_$HIST_VIEW.sql"

echo "$custom_query" > $CUSTOM_file

if ! /cevac/scripts/exec_sql_script.sh "$CUSTOM_file" ; then
  error="Could not execute CEVAC_CUSTOM_HIST"
  /cevac/scripts/log_error.sh "$error"
  exit 1
fi
