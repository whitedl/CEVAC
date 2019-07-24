IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_CACHE_APPEND') DROP PROCEDURE CEVAC_CACHE_APPEND;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_CACHE_APPEND
	@tables NVARCHAR(1000),
	@destTableName NVARCHAR(300) = NULL
AS

DECLARE @execute int;
SET @execute = 1;

DECLARE @name NVARCHAR(300);
DECLARE @name_CACHE NVARCHAR(300);
DECLARE @Alias_or_PSID NVARCHAR(50);
DECLARE @select_query NVARCHAR(MAX);
DECLARE @i INT;
DECLARE @IDName NVARCHAR(50);
DECLARE @AliasName NVARCHAR(50);
DECLARE @DataName NVARCHAR(50);
DECLARE @DateTimeName NVARCHAR(50);
DECLARE @cevac_app_data NVARCHAR(300);
DECLARE @create_app_data NVARCHAR(MAX);
DECLARE @drop_app_data NVARCHAR(MAX);
DECLARE @row_count INT;
DECLARE @rows_transferred INT;
DECLARE @params_rc INT;

SET @cevac_app_data = 'CEVAC_APPEND_DATA';
SET @i = 100;
IF OBJECT_ID('dbo.#cevac_params', 'U') IS NOT NULL DROP TABLE #cevac_params;
SELECT * INTO #cevac_params FROM ListTable(@tables);
SET @params_rc = @@ROWCOUNT;
IF @params_rc > 1 AND @destTableName IS NOT NULL BEGIN
	RAISERROR('Custom append must have only one table', 11, 1);
	RETURN
END

IF OBJECT_ID(@cevac_app_data) IS NULL BEGIN
	SET @create_app_data = '
	CREATE TABLE ' + @cevac_app_data + '( 
		name NVARCHAR(300),
		rows_transferred INT,
		runtime DATETIME
	);
	';
	EXEC(@create_app_data);
END

DECLARE @custom BIT;
SET @custom = 0;
IF @destTableName IS NOT NULL BEGIN 
	SET @i = 1;
	SET @custom = 1;
	SET @name_CACHE = @destTableName;
END ELSE BEGIN
	SET @name = NULL;
	SET @name_CACHE = NULL;
END
WHILE (EXISTS(SELECT 1 FROM #cevac_params) AND @i > 0) BEGIN
	SET @i = @i - 1;
	
	SET @name = (SELECT TOP 1 * FROM #cevac_params);
	DELETE TOP(1) FROM #cevac_params;

	IF @custom = 0 AND @name_CACHE IS NULL BEGIN
		-- Replace _VIEW with _CACHE, else append _CACHE
		SET @name_CACHE = REPLACE(@name, '_VIEW', '');
		SET @name_CACHE = @name_CACHE + '_CACHE';
	END
	SELECT @name_CACHE AS 'CACHE Table name';

	EXEC CEVAC_ALIAS_OR_PSID_OUTPUT @table = @name, @Alias_or_PSID_out = @Alias_or_PSID OUTPUT;
	SET @DateTimeName = ISNULL((SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE TableName = @name), 'UTCDateTime');
	SET @IDName = ISNULL((SELECT TOP 1 RTRIM(IDName) FROM CEVAC_TABLES WHERE TableName = @name), 'PointSliceID');
	SET @AliasName = ISNULL((SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE TableName = @name), 'Alias');
	SET @DataName = ISNULL((SELECT TOP 1 RTRIM(DataName) FROM CEVAC_TABLES WHERE TableName = @name),'ActualValue');

	DECLARE @now DATETIME;
	SET @now = (SELECT GETUTCDATE());

	DECLARE @where_subquery NVARCHAR(300);
	DECLARE @select_or_insert NVARCHAR(30);
	SET @select_or_insert = 'SELECT';
	-- Default: clone _VIEW into _HIST
	SET @select_query = '
	DECLARE @rows_transferred INT;
	DECLARE @now DATETIME;
	SET @now = ''' + CAST(@now AS NVARCHAR(100)) + ''';
	SELECT * INTO ' + @name_CACHE + ' FROM ' + @name + '
	
	SET @rows_transferred = @@ROWCOUNT;

	IF EXISTS (SELECT * FROM ' + @cevac_app_data + ' WHERE name = ''' + @name + ''') BEGIN
		UPDATE ' + @cevac_app_data + '
		SET rows_transferred = @rows_transferred, runtime = @now
		WHERE name = ''' + @name + '''
	END ELSE BEGIN
		INSERT INTO ' + @cevac_app_data + '(name, rows_transferred, runtime)
		VALUES (
			''' + @name + ''', @rows_transferred, @now
		)
	END
	';

	-- if cache exists, only grab latest data
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME=@name_CACHE) BEGIN
		DECLARE @update_time DATETIME;
		SET @update_time = ISNULL((SELECT TOP 1 update_time FROM CEVAC_CACHE_RECORDS WHERE table_name = @name AND storage = 'SQL' ORDER BY update_time DESC),CAST(0 AS DATETIME));
		--SET @where_subquery = ' WHERE UTCDateTime BETWEEN ' + '''' + CAST(@update_time AS NVARCHAR(50)) + '''' + ' AND ' + '''' + CAST(@now AS NVARCHAR(50)) + '''';
--		SET @where_subquery = ' WHERE UTCDateTime BETWEEN @update_time AND @now';
		SET @select_or_insert = 'INSERT';
	
		DECLARE @begin DATETIME;
		SET @begin = DATEADD(MONTH, -1, @now);		

		IF DATEDIFF(day, @update_time, @begin) > 0 BEGIN
			SET @begin = DATEADD(MONTH, -1, @update_time);
		END

		IF @begin < CAST(0 AS DATETIME) SET @begin = CAST(0 AS DATETIME);

		SET @select_query = ' ' +
		'
		DECLARE @now DATETIME; SET @now = ''' + CAST(@now AS NVARCHAR(100)) +  '''; 
		DECLARE @begin DATETIME; SET @begin = ''' + CAST(@begin AS NVARCHAR(100)) +  ''';
		DECLARE @rows_transferred INT;

		WITH V AS (
			SELECT * FROM ' + @name + ' WHERE ' + @DateTimeName + ' BETWEEN @begin AND @now
		), C AS (
			SELECT * FROM ' + @name_CACHE + ' WHERE ' + @DateTimeName + ' BETWEEN @begin AND @now
		)
		INSERT INTO ' + @name_CACHE +
		'
		SELECT V.* FROM V ' +
		'LEFT JOIN C ON V.' + @DateTimeName + ' = C.' + @DateTimeName + ' AND V.' + @IDName + ' = C.' + @IDName
		+ ' WHERE C.' + @DateTimeName + ' IS NULL AND C.' + @IDName + ' IS NULL

		SET @rows_transferred = @@ROWCOUNT;

		IF EXISTS (SELECT * FROM ' + @cevac_app_data + ' WHERE name = ''' + @name + ''') BEGIN
			UPDATE ' + @cevac_app_data + '
			SET rows_transferred = @rows_transferred, runtime = @now
			WHERE name = ''' + @name + '''
		END ELSE BEGIN
			INSERT INTO ' + @cevac_app_data + '(name, rows_transferred, runtime)
			VALUES (
				''' + @name + ''', @rows_transferred, @now
			)
		END
		';

	END;

	PRINT @select_query;
	IF @execute = 1 BEGIN
		EXEC(@select_query);
		-- insert into CEVAC_TABLES
		IF EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @name) BEGIN
			DECLARE @BuildingSName NVARCHAR(100);
			DECLARE @Metric NVARCHAR(100);
			DECLARE @Age NVARCHAR(100);
			DECLARE @isCustom BIT;
			DECLARE @customLASR BIT;

			SET @BuildingSName = (SELECT BuildingSName FROM CEVAC_TABLES WHERE TableName = @name);
			SET @Metric = (SELECT Metric FROM CEVAC_TABLES WHERE TableName = @name);
			SET @Age = (SELECT Age FROM CEVAC_TABLES WHERE TableName = @name);
			SET @isCustom = (SELECT isCustom FROM CEVAC_TABLES WHERE TableName = @name);
			SET @customLASR = (SELECT customLASR FROM CEVAC_TABLES WHERE TableName = @name);

			IF @BuildingSName IS NULL BEGIN
				RAISERROR('BuildingSName is NULL',11,1);
				RETURN
			END
			IF @Metric IS NULL BEGIN
				RAISERROR('Metric is NULL',11,1);
				RETURN
			END
			IF @Age IS NULL BEGIN
				RAISERROR('Age is NULL',11,1);
				RETURN
			END
			IF @isCustom IS NULL BEGIN
				RAISERROR('isCustom is NULL',11,1);
				RETURN
			END
			IF @customLASR IS NULL BEGIN
				RAISERROR('customLASR is NULL',11,1);
				RETURN
			END

			DELETE FROM CEVAC_TABLES WHERE TableName = @name_CACHE;
			INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Dependencies, customLASR)
				VALUES (
					@BuildingSName,
					@Metric,
					@Age,
					@name_CACHE,
					@DateTimeName,
					@IDName,
					@AliasName,
					@DataName,
					@isCustom,
					@name,
					@customLASR
				)
		END
	END


	SET @row_count = (
		SELECT SUM (row_count)
		FROM sys.dm_db_partition_stats
		WHERE object_id=OBJECT_ID(@name_CACHE)   
--		AND (index_id=0 or index_id=1);
	);
	SET @rows_transferred = ISNULL((SELECT TOP 1 rows_transferred FROM CEVAC_APPEND_DATA WHERE name = @name ORDER BY runtime DESC),@row_count);	

	DECLARE @rows_transferred_string NVARCHAR(100);
	DECLARE @row_count_string NVARCHAR(100);

	SET @row_count_string = ISNULL(CAST(@row_count AS nvarchar(30)), '-1');
	-- If rows_transferred is NULL, set equal to row_count (e.g. table has been rebuilt)
	SET @rows_transferred_string = ISNULL(CAST(@rows_transferred AS nvarchar(30)), @row_count_string);

	DECLARE @cache_query NVARCHAR(MAX);
	SET @cache_query = '
	DECLARE @last_UTC DATETIME;
	SET @last_UTC = ISNULL((SELECT TOP 1 ' + @DateTimeName + ' FROM ' + @name_CACHE + ' ORDER BY ' + @DateTimeName + ' DESC), CAST(0 AS DATETIME));


	INSERT INTO CEVAC_CACHE_RECORDS(table_name, update_time, storage, last_UTC, row_count, rows_transferred) VALUES ('''
	+ isnull(@name,'NAME_NULL') + ''', ''' + CAST(@now AS nvarchar(100)) + ''', ''SQL'', @last_UTC, ' + @row_count_string + ', ' + @rows_transferred_string + ' )';

	PRINT @cache_query;
	IF @execute = 1 EXEC(@cache_query);


	-- rebuild _HIST API
	IF @name_CACHE LIKE '%HIST_CACHE%' AND @custom = 0 BEGIN
		IF OBJECT_ID(REPLACE(@name_CACHE, '_CACHE', ''), 'V') IS NOT NULL BEGIN
		DECLARE @drop_HIST NVARCHAR(MAX);
		SET @drop_HIST = 'DROP VIEW ' + REPLACE(@name_CACHE, '_CACHE', '');
		
		SELECT @drop_HIST AS 'Drop _HIST';
		IF @execute = 1 EXEC(@drop_HIST);
		END
		DECLARE @Create_view NVARCHAR(MAX);
		SET @Create_view = '
		CREATE VIEW ' + REPLACE(@name_CACHE, '_CACHE', '') + '
		AS SELECT * FROM ' + @name_CACHE;
		SELECT @Create_view AS 'Rebuild _HIST API';
		IF @execute = 1 EXEC(@Create_view);

	END
	-- set to NULL for custom tables
	SET @name = NULL;
	SET @name_CACHE = NULL;
END

