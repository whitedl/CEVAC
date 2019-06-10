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
DECLARE @select_query NVARCHAR(500);
DECLARE @i INT;
SET @i = 20;
IF OBJECT_ID('dbo.#cevac_params', 'U') IS NOT NULL DROP TABLE #cevac_params;
SELECT * INTO #cevac_params FROM ListTable(@tables);
WHILE (EXISTS(SELECT 1 FROM #cevac_params) AND @i > 0) BEGIN
	SET @i = @i - 1;
	SET @name = (SELECT TOP 1 * FROM #cevac_params);
	DELETE TOP(1) FROM #cevac_params;
--	SELECT COUNT(*) FROM #cevac_params;

	-- Replace _VIEW with _CACHE, else append _CACHE
	SET @name_CACHE = REPLACE(@name, '_VIEW', '');
	SET @name_CACHE = @name_CACHE + '_CACHE';
	SELECT @name_CACHE AS 'CACHE Table name';


--	DECLARE @where_subquery NVARCHAR(50);
	DECLARE @now DATETIME;
	SET @now = (SELECT GETUTCDATE());

	DECLARE @where_subquery NVARCHAR(300);
	DECLARE @select_or_insert NVARCHAR(30);
	SET @select_or_insert = 'SELECT';
	SET @select_query = 'SELECT * INTO ' + @name_CACHE + ' FROM ' + @name;

	-- if cache exists, 
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME=@name_CACHE) BEGIN
		DECLARE @update_time DATETIME;
		SET @update_time = (SELECT TOP 1 update_time FROM CEVAC_CACHE_RECORDS WHERE table_name = @name ORDER BY update_time DESC);
		SET @where_subquery = ' WHERE UTCDateTime BETWEEN ' + '''' + CAST(@update_time AS NVARCHAR(50)) + '''' + ' AND ' + '''' + CAST(@now AS NVARCHAR(50)) + '''';
		SET @select_or_insert = 'INSERT';
	
		SET @select_query = 'INSERT INTO ' + @name_CACHE + ' SELECT * FROM ' + @name	
		 + ' ' + isnull(@where_subquery, '');
	
	
--		DECLARE @ExecSQL NVARCHAR(300);
--		SET @ExecSQL = CONCAT('DROP TABLE ', @name_CACHE);
--		EXEC(@ExecSQL);
	END;

	SELECT @select_query AS 'Select Query';
	IF @execute = 1 EXEC(@select_query);

	DECLARE @cache_query NVARCHAR(300);
	SET @cache_query = 'INSERT INTO CEVAC_CACHE_RECORDS(table_name, update_time) VALUES (''' + @name +''', ''' + CAST(@now AS nvarchar(50)) + ''')';

	SELECT @cache_query AS 'Cache query';
	IF @execute = 1 EXEC(@cache_query);


	-- rebuild _HIST API
	IF @name_CACHE LIKE '%HIST%' BEGIN
		IF OBJECT_ID(REPLACE(@name_CACHE, '_CACHE', ''), 'V') IS NOT NULL BEGIN
		DECLARE @drop_HIST NVARCHAR(70);
		SET @drop_HIST = 'DROP VIEW ' + REPLACE(@name_CACHE, '_CACHE', '');
		
		SELECT @drop_HIST AS 'Drop _HIST';
		IF @execute = 1 EXEC(@drop_HIST);
		END
		DECLARE @Create_view NVARCHAR(100);
		SET @Create_view = '
		CREATE VIEW ' + REPLACE(@name_CACHE, '_CACHE', '') + '
		AS SELECT * FROM ' + @name_CACHE;
		SELECT @Create_view AS 'Rebuild _HIST API';
		IF @execute = 1 EXEC(@Create_view);

	END

END
