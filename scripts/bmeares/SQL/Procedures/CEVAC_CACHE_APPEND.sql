IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_CACHE_APPEND') DROP PROCEDURE CEVAC_CACHE_APPEND;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_CACHE_APPEND
	@tables NVARCHAR(500)
AS

DECLARE @execute int;
SET @execute = 1;

DECLARE @name NVARCHAR(50);
DECLARE @name_CACHE NVARCHAR(50);
DECLARE @Alias_or_PSID NVARCHAR(50);
DECLARE @select_query NVARCHAR(MAX);
DECLARE @i INT;
DECLARE @AliasName NVARCHAR(50);
DECLARE @DateTimeName NVARCHAR(50);
SET @i = 100;
IF OBJECT_ID('dbo.#cevac_params', 'U') IS NOT NULL DROP TABLE #cevac_params;
SELECT * INTO #cevac_params FROM ListTable(@tables);


WHILE (EXISTS(SELECT 1 FROM #cevac_params) AND @i > 0) BEGIN
	IF OBJECT_ID('dbo.cevac_temp', 'U') IS NOT NULL DROP TABLE cevac_temp;
	CREATE TABLE cevac_temp (
	name NVARCHAR(100),
	--row_count int,
	rows_transferred int,
	runtime DATETIME
	);
	
	SET @i = @i - 1;
	SET @name = (SELECT TOP 1 * FROM #cevac_params);
	DELETE TOP(1) FROM #cevac_params;
--	SELECT COUNT(*) FROM #cevac_params;

	-- Replace _VIEW with _CACHE, else append _CACHE
	SET @name_CACHE = REPLACE(@name, '_VIEW', '');
	SET @name_CACHE = @name_CACHE + '_CACHE';
	SELECT @name_CACHE AS 'CACHE Table name';
	EXEC CEVAC_ALIAS_OR_PSID_OUTPUT @table = @name, @Alias_or_PSID_out = @Alias_or_PSID OUTPUT
	SET @DateTimeName = (SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE TableName = @name);
	SET @AliasName = (SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE TableName = @name);

--	DECLARE @where_subquery NVARCHAR(50);
	DECLARE @now DATETIME;
	SET @now = (SELECT GETUTCDATE());

	DECLARE @where_subquery NVARCHAR(300);
	DECLARE @select_or_insert NVARCHAR(30);
	SET @select_or_insert = 'SELECT';
	-- Default: clone _VIEW into _HIST
	SET @select_query = 'SELECT * INTO ' + @name_CACHE + ' FROM ' + @name;

	-- if cache exists, only grab latest data
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME=@name_CACHE) BEGIN
		DECLARE @update_time DATETIME;
		SET @update_time = (SELECT TOP 1 update_time FROM CEVAC_CACHE_RECORDS WHERE table_name = @name AND storage = 'SQL' ORDER BY update_time DESC);
		--SET @where_subquery = ' WHERE UTCDateTime BETWEEN ' + '''' + CAST(@update_time AS NVARCHAR(50)) + '''' + ' AND ' + '''' + CAST(@now AS NVARCHAR(50)) + '''';
--		SET @where_subquery = ' WHERE UTCDateTime BETWEEN @update_time AND @now';
		SET @select_or_insert = 'INSERT';
	
		DECLARE @begin DATETIME;
		SET @begin = DATEADD(day, -31, @now);		

		IF DATEDIFF(day, @update_time, @begin) > 0 BEGIN
			SET @begin = DATEADD(day, -31,@update_time);
		END

		SET @select_query = ' ' +
--		'DECLARE @update_time DATETIME; SET @update_time = ''' + CAST(@update_time AS NVARCHAR(50)) +  '''; ' +
		'
		DECLARE @now DATETIME; SET @now = ''' + CAST(@now AS NVARCHAR(50)) +  '''; 
		DECLARE @begin DATETIME; SET @begin = ''' + CAST(@begin AS NVARCHAR(50)) +  ''';


		WITH V AS (
			SELECT * FROM ' + @name + ' WHERE ' + @DateTimeName + ' BETWEEN @begin AND @now
		), C AS (
			SELECT * FROM ' + @name_CACHE + ' WHERE ' + @DateTimeName + ' BETWEEN @begin AND @now
		)
		INSERT INTO ' + @name_CACHE +
		'
		SELECT V.* FROM V ' +
		'LEFT JOIN C ON V.' + @DateTimeName + ' = C.' + @DateTimeName + ' AND V.' + @AliasName + ' = C.' + @AliasName
		+ ' WHERE C.' + @DateTimeName + ' IS NULL AND C.' + @AliasName + ' IS NULL;

		INSERT INTO cevac_temp (name, rows_transferred, runtime)
		VALUES (
			''' + @name_CACHE + ''', @@ROWCOUNT, GETUTCDATE()
		)';
	
	
--		DECLARE @ExecSQL NVARCHAR(300);
--		SET @ExecSQL = CONCAT('DROP TABLE ', @name_CACHE);
--		EXEC(@ExecSQL);
	END;

	SELECT @select_query AS 'Select Query';
	IF @execute = 1 BEGIN
		EXEC(@select_query);
		-- insert into CEVAC_TABLES
		IF EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @name) BEGIN
			DECLARE @BuildingSName NVARCHAR(100);
			DECLARE @Metric NVARCHAR(100);
			DECLARE @Age NVARCHAR(100);
			DECLARE @isCustom BIT;

			SET @BuildingSName = (SELECT BuildingSName FROM CEVAC_TABLES WHERE TableName = @name);
			SET @Metric = (SELECT Metric FROM CEVAC_TABLES WHERE TableName = @name);
			SET @Age = (SELECT Age FROM CEVAC_TABLES WHERE TableName = @name);
			SET @isCustom = (SELECT isCustom FROM CEVAC_TABLES WHERE TableName = @name);


			DELETE FROM CEVAC_TABLES WHERE TableName = @name_CACHE;
			INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, isCustom, Dependencies)
				VALUES (
					@BuildingSName,
					@Metric,
					@Age,
					@name_CACHE,
					@DateTimeName,
					@AliasName,
					@isCustom,
					@name
				)
		END
	END

	DECLARE @row_count INT;
	DECLARE @rows_transferred INT;
	SET @row_count = (
		SELECT SUM (row_count)
		FROM sys.dm_db_partition_stats
		WHERE object_id=OBJECT_ID(@name_CACHE)   
--		AND (index_id=0 or index_id=1);
	);
	SET @rows_transferred = (SELECT TOP 1 rows_transferred FROM cevac_temp WHERE name = @name_CACHE ORDER BY runtime DESC);	

	DECLARE @cache_query NVARCHAR(MAX);
	SET @cache_query = '
	DECLARE @last_UTC DATETIME;
	SET @last_UTC = (SELECT TOP 1 ' + @DateTimeName + ' FROM ' + @name_CACHE + ' ORDER BY ' + @DateTimeName + ' DESC);


	INSERT INTO CEVAC_CACHE_RECORDS(table_name, update_time, storage, last_UTC, row_count, rows_transferred) VALUES ('''
	+ @name + ''', ''' + CAST(@now AS nvarchar(50)) + ''', ''SQL'', @last_UTC, ' + isnull(CAST(@row_count AS nvarchar(20)), '-1') + ', ' + isnull(CAST(@rows_transferred AS nvarchar(30)), '-1') + ' )';

	SELECT @cache_query AS 'Cache query';
	IF @execute = 1 EXEC(@cache_query);


	-- rebuild _HIST API
	IF @name_CACHE LIKE '%HIST%' BEGIN
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

	DROP TABLE cevac_temp;
END

