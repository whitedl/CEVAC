IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_RECORD_COUNTS') DROP PROCEDURE CEVAC_RECORD_COUNTS;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_RECORD_COUNTS
	@BuildingSName NVARCHAR(100),
	@Metric NVARCHAR(100)
AS
DECLARE @insert_sql NVARCHAR(MAX);
DECLARE @CEVAC_ALL_RECORD_COUNT_HIST_RAW NVARCHAR(200);
SET @insert_sql = '
DELETE FROM ' + @CEVAC_ALL_RECORD_COUNT_HIST_RAW + '
WHERE BuildingSName = ''' + @BuildingSName + ''' AND Metric = ''' + @Metric + ''';

WITH dateparts AS (
	SELECT DATEPART(YEAR, UTCDateTime) AS yr, DATEPART(MONTH, UTCDateTime) AS mth
	FROM CEVAC_WATT_IAQ_HIST
), grouped_dateparts AS (
	SELECT * FROM dateparts
	GROUP BY yr, mth
), months AS (
	SELECT DATEFROMPARTS ( yr, mth, 1 ) AS combined
	FROM grouped_dateparts  
), monthly_counts AS (
	SELECT g.yr, g.mth, COUNT(h.UTCDateTime) AS mth_record_count
	FROM CEVAC_WATT_IAQ_HIST AS h
	INNER JOIN grouped_dateparts AS g ON g.mth = DATEPART(MONTH, h.UTCDateTime) AND g.yr = DATEPART(YEAR, h.UTCDateTime)
	WHERE UTCDateTime BETWEEN DATEFROMPARTS(g.yr, g.mth, 1) AND DATEADD(DAY,1,EOMONTH(DATEFROMPARTS(g.yr, g.mth, 1)))
	GROUP BY g.yr, g.mth
), total_sums AS (
	SELECT mc.yr, mc.mth, SUM(mth_record_count) AS total_sum
	FROM monthly_counts AS mc
	GROUP BY mc.yr, mc.mth
)
SELECT DATEFROMPARTS(mc.yr, mc.mth,1) AS Year_month, mc.mth_record_count AS Growth, SUM(mc.mth_record_count) OVER (ORDER BY mc.yr, mc.mth) AS Record_count 
INTO ' + @CEVAC_ALL_RECORD_COUNT_HIST_RAW + '
FROM monthly_counts AS mc
';







