#! /bin/sh

query="
IF OBJECT_ID('CEVAC_TABLES_BACKUP_INT') IS NOT NULL DROP TABLE CEVAC_TABLES_BACKUP_INT;
SELECT * INTO CEVAC_TABLES_BACKUP_INT FROM CEVAC_TABLES;
"
if ! /cevac/scripts/exec_sql.sh "$query"; then
  error="Failed to backup intermediary CEVAC_TABLES!"
  /cevac/scripts/log_error.sh "$error" "CEVAC_TABLES_BACKUP_INT"
  exit 1
fi

query="
IF OBJECT_ID('CEVAC_TABLES_BACKUP') IS NOT NULL DROP TABLE CEVAC_TABLES_BACKUP;
SELECT * INTO CEVAC_TABLES_BACKUP FROM CEVAC_TABLES;
"
if ! /cevac/scripts/exec_sql.sh "$query"; then
  error="Failed to backup CEVAC_TABLES!"
  /cevac/scripts/log_error.sh "$error" "CEVAC_TABLES_BACKUP"
  exit 1
fi

/cevac/scripts/log_activity.sh -t "CEVAC_TABLES"
