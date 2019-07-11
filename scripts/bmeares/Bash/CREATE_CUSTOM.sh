#! /bin/sh
# ./seperator.sh
BuildingSName="$1"
Metric="$2"
DateTimeName="$3"
AliasName="$4"
Dependencies="$5"

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] ; then
  echo "Usage: $0 [BuildingSName] [Metric] [DateTimeName] [AliasName] [Dependencies]"
  echo $'Enter the table information.\n'
  echo $'Building            (e.g. WATT): '; read BuildingSName
  echo $'Metric              (e.g. TEMP): '; read Metric
  echo $'DateTimeName (e.g. UTCDateTime):'; read DateTimeName
  echo $'AliasName        (e.g. : Alias):'; read AliasName
  echo $'Dependencies   (comma-separated):'; read Dependencies
fi
# Dependencies="'"$Dependencies"'"
HIST_VIEW="CEVAC_$BuildingSName""_$Metric"_"HIST_VIEW"

def_file="/cevac/CUSTOM_DEFS/$HIST_VIEW.sql"
if [ ! -f "$def_file" ]; then
  echo "$def_file is missing"
  exit 1
fi

CREATE_VIEW="
CREATE VIEW $HIST_VIEW AS
"

Definition=`cat $def_file | sed "s/'/''/g"`
Definition="$CREATE_VIEW $Definition"

# Insert into CEVAC_TABLES
cevac_tables_query="
DELETE FROM CEVAC_TABLES WHERE TableName = '$HIST_VIEW';
INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, isCustom, Definition, Dependencies)
  VALUES (
    '$BuildingSName',
    '$Metric',
    'HIST',
    '$HIST_VIEW',
    '$DateTimeName',
    '$AliasName',
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

/cevac/scripts/exec_sql_script.sh "$CUSTOM_file"
