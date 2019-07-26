IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_RECORD_COUNTS') DROP PROCEDURE CEVAC_RECORD_COUNTS;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_RECORD_COUNTS
	@BuildingSName NVARCHAR(100),
	@Metric NVARCHAR(100)
AS
DECLARE @execute BIT;
SET @execute = 1;
DECLARE @insert_sql NVARCHAR(MAX);
DECLARE @CEVAC_ALL_RECORD_COUNT_HIST_RAW NVARCHAR(200);
SET @CEVAC_ALL_RECORD_COUNT_HIST_RAW = 'CEVAC_ALL_RECORDS_COUNTS_COMPARE_HIST_RAW';
DECLARE @HIST NVARCHAR(400);

SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';

DECLARE @DateTimeName NVARCHAR(100);
SET @DateTimeName = RTRIM((SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE BuildingSName = @BuildingSName AND Metric = @Metric AND Age = 'HIST'));

IF @DateTimeName IS NULL BEGIN
	RAISERROR('DateTimeName is null', 11, 1);
	RETURN
END
IF @HIST IS NULL BEGIN
	RAISERROR('HIST is null', 11, 1);
	RETURN
END
IF @BuildingSName IS NULL BEGIN
	RAISERROR('BuildingSName is null', 11, 1);
	RETURN
END
IF @CEVAC_ALL_RECORD_COUNT_HIST_RAW IS NULL BEGIN
	RAISERROR('CEVAC_ALL_RECORD_COUNT_HIST_RAW is null', 11, 1);
	RETURN
END

IF OBJECT_ID(@CEVAC_ALL_RECORD_COUNT_HIST_RAW) IS NULL BEGIN
		CREATE TABLE CEVAC_ALL_RECORDS_COUNTS_COMPARE_HIST_RAW (
		Year_month DATE NOT NULL,
		BuildingSName NVARCHAR(50) NOT NULL,
		Metric NVARCHAR(50) NOT NULL,
		Growth INT NOT NULL,
		Record_count INT NOT NULL
	);
END


SET @insert_sql = '
DELETE FROM ' + @CEVAC_ALL_RECORD_COUNT_HIST_RAW + '
WHERE BuildingSName = ''' + @BuildingSName + ''' AND Metric = ''' + @Metric + ''';

WITH dateparts AS (
	SELECT DATEPART(YEAR, ' + @DateTimeName + ') AS yr, DATEPART(MONTH, ' + @DateTimeName + ') AS mth
	FROM ' + @HIST + '
), grouped_dateparts AS (
	SELECT * FROM dateparts
	GROUP BY yr, mth
), months AS (
	SELECT DATEFROMPARTS ( yr, mth, 1 ) AS combined
	FROM grouped_dateparts  
), monthly_counts AS (
	SELECT g.yr, g.mth, COUNT(h.' + @DateTimeName + ') AS mth_record_count
	FROM ' + @HIST + ' AS h
	INNER JOIN grouped_dateparts AS g ON g.mth = DATEPART(MONTH, h.' + @DateTimeName + ') AND g.yr = DATEPART(YEAR, h.' + @DateTimeName + ')
	WHERE ' + @DateTimeName + ' BETWEEN DATEFROMPARTS(g.yr, g.mth, 1) AND DATEADD(DAY,1,EOMONTH(DATEFROMPARTS(g.yr, g.mth, 1)))
	GROUP BY g.yr, g.mth
), total_sums AS (
	SELECT mc.yr, mc.mth, SUM(mth_record_count) AS total_sum
	FROM monthly_counts AS mc
	GROUP BY mc.yr, mc.mth
)
INSERT INTO ' + @CEVAC_ALL_RECORD_COUNT_HIST_RAW + '
SELECT DATEFROMPARTS(mc.yr, mc.mth,1) AS Year_month, ''' + @BuildingSName + ''' AS BuildingSName, ''' + @Metric + ''' AS Metric, mc.mth_record_count AS Growth, SUM(mc.mth_record_count) OVER (ORDER BY mc.yr, mc.mth) AS Record_count 
FROM monthly_counts AS mc
';

--PRINT @insert_sql;
--SELECT @insert_sql;
IF @execute = 1 EXEC(@insert_sql);


