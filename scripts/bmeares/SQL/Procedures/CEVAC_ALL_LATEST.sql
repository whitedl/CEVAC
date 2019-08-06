IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_ALL_LATEST') DROP PROCEDURE CEVAC_ALL_LATEST;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_ALL_LATEST
	@Metric NVARCHAR(200),
	@execute BIT = 1
AS
DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);
DECLARE @error NVARCHAR(MAX);

DECLARE @source_Metric NVARCHAR(MAX);
SET @source_Metric = @Metric;
SET @Metric = @Metric + '_LATEST';
DECLARE	@BuildingSName NVARCHAR(200);
DECLARE @buildings TABLE(BuildingSName NVARCHAR(200));
DECLARE @b_LATEST NVARCHAR(MAX);
DECLARE @b_DateTimeName NVARCHAR(MAX);
DECLARE @b_DataName NVARCHAR(MAX);
DECLARE @b_AliasName NVARCHAR(MAX);
DECLARE @b_IDName NVARCHAR(MAX);

DECLARE @DateTimeName NVARCHAR(MAX);
DECLARE @DataName NVARCHAR(MAX);
DECLARE @AliasName NVARCHAR(MAX);
DECLARE @IDName NVARCHAR(MAX);
DECLARE @isCustom BIT;
DECLARE @customLASR BIT;

SET @DateTimeName = 'UTCDateTime';
SET @DataName = 'ActualValue';
SET @AliasName = 'Alias';
SET @IDName = 'PointSliceID';
SET @isCustom = 1;
SET @customLASR = 0;

DECLARE @HIST NVARCHAR(MAX);
SET @HIST = 'CEVAC_ALL_' + @Metric + '_HIST';
DECLARE @HIST_VIEW NVARCHAR(MAX);
SET @HIST_VIEW = @HIST + '_VIEW';
DECLARE @HIST_CACHE NVARCHAR(MAX);
SET @HIST_CACHE = @HIST + '_CACHE';
DECLARE @EXEC_SQL NVARCHAR(MAX);

IF OBJECT_ID(@HIST_CACHE) IS NOT NULL BEGIN
	SET @EXEC_SQL = 'DROP TABLE ' + @HIST_CACHE;
	PRINT @EXEC_SQL;
	IF @execute = 1 EXEC(@EXEC_SQL);
END
IF OBJECT_ID(@HIST) IS NOT NULL BEGIN
	SET @EXEC_SQL = 'DROP VIEW ' + @HIST;
	PRINT @EXEC_SQL;
	IF @execute = 1 EXEC(@EXEC_SQL);
END
IF OBJECT_ID(@HIST_VIEW) IS NOT NULL BEGIN
	SET @EXEC_SQL = 'DROP VIEW ' + @HIST_VIEW;
	PRINT @EXEC_SQL;
	IF @execute = 1 EXEC(@EXEC_SQL);
END

INSERT INTO @buildings SELECT DISTINCT RTRIM(BuildingSName) AS BuildingSName FROM CEVAC_TABLES WHERE Metric = @source_Metric AND TableName LIKE '%HIST_VIEW%' AND NOT BuildingSName = 'ALL';
DECLARE @Definition NVARCHAR(MAX);
DECLARE @Dependencies NVARCHAR(MAX);
DECLARE @union_subquery NVARCHAR(MAX);
SET @Definition = '
CREATE VIEW ' + @HIST_VIEW + ' AS
';
SET @Dependencies = '';

DECLARE @i INT;
SET @i = 10000;
WHILE EXISTS (SELECT 1 FROM @buildings) AND @i > 0 BEGIN
	SET @BuildingSName = (SELECT TOP 1 BuildingSName FROM @buildings);
	DELETE TOP(1) FROM @buildings;
	SET @i = @i - 1;
	SET @b_LATEST = 'CEVAC_' + @BuildingSName + '_' + @source_Metric + '_LATEST';

	SET @b_DateTimeName = (SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE TableName = @b_LATEST);
	SET @b_DataName = (SELECT TOP 1 RTRIM(DataName) FROM CEVAC_TABLES WHERE TableName = @b_LATEST);
	SET @b_AliasName = (SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE TableName = @b_LATEST);
	SET @b_IDName = (SELECT TOP 1 RTRIM(IDName) FROM CEVAC_TABLES WHERE TableName = @b_LATEST);

	SET @union_subquery = '
	SELECT b.' + @b_IDName + ' AS ''' + @IDName + ''', b.' + @b_AliasName + ' AS ''' + @AliasName + ''', b.' + @b_DateTimeName + ' AS ''' + @DateTimeName
	 + ''', b.' + @b_DataName + ' AS ''' + @DataName + ''', ''' + @BuildingSName + ''' AS ''BuildingSName'' FROM ' + @b_LATEST + ' AS b
	UNION';
	SET @Definition = @Definition + @union_subquery;
	SET @Dependencies = @Dependencies + @b_LATEST + ',';
END

SET @Definition = SUBSTRING(@Definition, 1, LEN(@Definition) - LEN('UNION'));
SET @Dependencies = SUBSTRING(@Dependencies, 1, LEN(@Dependencies) - LEN(','));

PRINT @Definition;

IF @execute = 1 BEGIN
	DELETE FROM CEVAC_TABLES WHERE TableName = @HIST_VIEW;
	INSERT INTO CEVAC_TABLES(BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Definition, Dependencies, customLASR)
	VALUES (
		'ALL',
		@Metric,
		'HIST',
		@HIST_VIEW,
		@DateTimeName,
		@IDName,
		@AliasName,
		@DataName,
		@isCustom,
		@Definition,
		@Dependencies,
		@customLASR
	);

--	EXEC(@Definition);
	EXEC CEVAC_CUSTOM_HIST @BuildingSName = 'ALL', @Metric = @Metric;
	EXEC CEVAC_VIEW @Building = 'ALL', @Metric = @Metric, @Age = 'HIST';
	EXEC CEVAC_VIEW @Building = 'ALL', @Metric = @Metric, @Age = 'LATEST';
END
