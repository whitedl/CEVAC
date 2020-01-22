#! /bin/sh

! /cevac/scripts/check_lock.sh && exit 1
/cevac/scripts/lock.sh

sql="
DECLARE @threshold DATETIME;
SET @threshold = DATEADD(month, -1, GETUTCDATE());
DELETE FROM CEVAC_ACTIVITY_LOG
WHERE UTCDateTime < @threshold;
"
if ! /cevac/scripts/exec_sql.sh "$sql" ; then
  error="Could not delete old records from CEVAC_ACTIVITY_LOG"
  /cevac/scripts/log_error.sh "$error" "CEVAC_ACTIVITY_LOG"
fi

sql="
DECLARE @threshold DATETIME;
SET @threshold = DATEADD(month, -1, GETUTCDATE());
DELETE FROM CEVAC_CACHE_RECORDS
WHERE update_time < @threshold;
"
if ! /cevac/scripts/exec_sql.sh "$sql" ; then
  error="Could not delete old records from CEVAC_ACTIVITY_LOG"
  /cevac/scripts/log_error.sh "$error" "CEVAC_ACTIVITY_LOG"
fi

sql="
DECLARE @threshold DATETIME;
SET @threshold = DATEADD(month, -6, GETUTCDATE());
DELETE FROM CEVAC_ERRORS
WHERE UTCDateTime < @threshold;
"
if ! /cevac/scripts/exec_sql.sh "$sql" ; then
  error="Could not delete old records from CEVAC_ERRORS"
  /cevac/scripts/log_error.sh "$error" "CEVAC_ERRORS"
fi

/cevac/scripts/unlock.sh

