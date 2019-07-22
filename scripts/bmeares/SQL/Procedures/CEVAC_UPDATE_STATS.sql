IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_UPDATE_STATS') DROP PROCEDURE CEVAC_UPDATE_STATS;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_UPDATE_STATS
	@BuildingSName NVARCHAR(50),
	@Metric NVARCHAR(50)
AS

DECLARE @execute BIT;
SET @execute = 1;

DECLARE @LATEST NVARCHAR(300);
SET @LATEST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_LATEST';
DECLARE @LATEST_CACHE NVARCHAR(300);
SET @LATEST_CACHE = @LATEST + '_CACHE';
DECLARE @stats_source NVARCHAR(300);
SET @stats_source = @LATEST_CACHE;

IF OBJECT_ID(@LATEST) IS NULL OR @LATEST IS NULL BEGIN
	DECLARE @error NVARCHAR(MAX);
	SET @error = @LATEST + ' does not exist';
	RAISERROR(@error, 11,1);
	RETURN;
END

DECLARE @DataName NVARCHAR(50);
SET @DataName = (SELECT TOP 1 DataName FROM CEVAC_TABLES WHERE TableName = @LATEST);

-- Create LATEST_CACHE
EXEC CEVAC_CACHE_INIT @tables = @LATEST;

DECLARE @EXEC_CALC NVARCHAR(MAX);
SET @EXEC_CALC = '
DECLARE @BuildingSName NVARCHAR(50);
SET @BuildingSName = ''' + @BuildingSName + ''';
DECLARE @Metric NVARCHAR(50);
SET @Metric = ''' + @Metric + ''';
DECLARE @DataName NVARCHAR(50);
SET @DataName = ''' + @DataName + ''';

DECLARE @avg_ FLOAT;
SET @avg_ = (SELECT AVG(CAST(' + @DataName + ' AS FLOAT)) FROM ' + @stats_source + ');
DECLARE @sum_ FLOAT;
SET @sum_ = (SELECT SUM(CAST(' + @DataName + ' AS FLOAT)) FROM ' + @stats_source + ');
DECLARE @min_ FLOAT;
SET @min_ = (SELECT MIN(CAST(' + @DataName + ' AS FLOAT)) FROM ' + @stats_source + ');
DECLARE @min_nz_ FLOAT;
SET @min_nz_ = (SELECT MIN(CAST(' + @DataName + ' AS FLOAT)) FROM ' + @stats_source + ' WHERE ' + @DataName + ' != 0);
DECLARE @max_ FLOAT;
SET @max_ = (SELECT MAX(CAST(' + @DataName + ' AS FLOAT)) FROM ' + @stats_source + ');

DECLARE @last_ETDateTime DATETIME;
DECLARE @update_UTC DATETIME;
DECLARE @update_ETDateTime DATETIME;
DECLARE @last_UTC DATETIME;
SET @last_UTC = (SELECT TOP 1 last_UTC FROM CEVAC_TABLES_RECORDS_COMPARE WHERE TableName = ''' + @LATEST + ''');
IF @last_UTC IS NOT NULL SET @last_ETDateTime = dbo.ConvertUTCToLocal(@last_UTC);
SET @update_UTC = (SELECT TOP 1 update_time FROM CEVAC_TABLES_RECORDS_COMPARE WHERE TableName = ''' + @LATEST + ''');
IF @update_UTC IS NOT NULL SET @update_ETDateTime = dbo.ConvertUTCToLocal(@update_UTC);

IF EXISTS (SELECT * FROM CEVAC_ALL_LATEST_STATS WHERE BuildingSName = @BuildingSName AND Metric = @Metric) BEGIN
	UPDATE CEVAC_ALL_LATEST_STATS
	SET DataName = @DataName, AVG = @avg_, SUM = @sum_, MIN = @min_, MIN_NZ = @min_nz_, MAX = @max_, last_ETDateTime = @last_ETDateTime, update_ETDateTime = @update_ETDateTime
	WHERE BuildingSName = @BuildingSName AND Metric = @Metric;
END ELSE BEGIN
	INSERT INTO CEVAC_ALL_LATEST_STATS (BuildingSName, Metric, DataName, AVG, SUM, MIN, MIN_NZ, MAX, last_ETDateTime, update_ETDateTime)
	VALUES(
		@BuildingSName,
		@Metric,
		@DataName,
		@avg_,
		@sum_,
		@min_,
		@min_nz_,
		@max_,
		@last_ETDateTime,
		@update_ETDateTime
	);
END

';

--PRINT @EXEC_CALC;
IF @execute = 1 BEGIN
	EXEC(@EXEC_CALC);
END
