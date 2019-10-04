IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_SP_AGG') DROP PROCEDURE CEVAC_SP_AGG;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_SP_AGG
	@ID NVARCHAR(100),
	@HIST NVARCHAR(300),
	@begin_UTC_string NVARCHAR(100),
	@now_UTC_string NVARCHAR(100),
	@DateTimeName NVARCHAR(100),
	@IDName NVARCHAR(100),
	@DataName NVARCHAR(100)
AS
DECLARE @execute BIT;
SET @execute = 1;

DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);
EXEC CEVAC_ACTIVITY @TableName = @HIST, @ProcessName = @ProcessName;

DECLARE @EXEC_SQL NVARCHAR(MAX);
SET @EXEC_SQL = '
DECLARE @now_UTC DATETIME;
DECLARE @last_UTC DATETIME;
DECLARE @begin_UTC DATETIME;
SET @now_UTC = CAST(''' + @now_UTC_string  + ''' AS DATETIME);
SET @begin_UTC = CAST(''' + @begin_UTC_string + ''' AS DATETIME);

WITH hist_slice AS (
	SELECT * FROM ' + @HIST + '
	WHERE ' + @DateTimeName + ' BETWEEN @begin_UTC AND @now_UTC
), agg AS (
	SELECT h.' + @IDName + ', h.Alias, h.UTCDateTime, h.ETDateTime, ROUND(h.ActualValue,2) AS ''ActualValue'', ROW_NUMBER() OVER (ORDER BY UTCDateTime) - ROW_NUMBER() OVER (PARTITION BY CAST(ActualValue AS INT) ORDER BY UTCDateTime) AS Grp
	FROM hist_slice AS h
	WHERE h.' + @IDName + ' = ' + @ID + '
), begin_records AS (
	SELECT ' + @IDName + ', Alias, MIN(' + @DateTimeName + ') AS ''' + @DateTimeName + ''', MIN(ETDateTime) AS ''ETDateTime'', ' + @DataName + '
	FROM agg
	GROUP BY ' + @IDName + ', Alias, grp, ' + @DataName + '
), end_records AS (
	SELECT ' + @IDname + ', Alias, MAX(' + @DateTimeName + ') AS ''' + @DateTimeName + ''', MAX(ETDateTime) AS ''ETDateTime'', ' + @DataName + '
	FROM agg
	GROUP BY ' + @IDName + ', Alias, grp, ' + @DataName + '
) SELECT * FROM begin_records
UNION SELECT * FROM end_records
';

IF @execute = 1 EXEC(@EXEC_SQL);

