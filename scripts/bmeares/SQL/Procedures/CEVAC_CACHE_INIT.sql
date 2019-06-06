IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_CACHE_INIT') DROP PROCEDURE CEVAC_CACHE_INIT;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_CACHE_INIT
	@tables NVARCHAR(500)
AS

DECLARE @name NVARCHAR(30);
DECLARE @name_CACHE NVARCHAR(30);
DECLARE @select_query NVARCHAR(200);
DECLARE @i INT;
SET @i = 20;
IF OBJECT_ID('dbo.#cevac_params', 'U') IS NOT NULL DROP TABLE #cevac_params;
SELECT * INTO #cevac_params FROM ListTable(@tables);
WHILE (EXISTS(SELECT 1 FROM #cevac_params) AND @i > 0) BEGIN
	SET @i = @i - 1;
	SET @name = (SELECT TOP 1 * FROM #cevac_params);
	DELETE TOP(1) FROM #cevac_params;
--	SELECT COUNT(*) FROM #cevac_params;
	SET @name_CACHE = @name + '_CACHE';
--	DECLARE @where_subquery NVARCHAR(50);
	DECLARE @now DATETIME;
	SET @now = (SELECT GETUTCDATE());


	-- if cache exists, 
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME=@name_CACHE) BEGIN
--		DECLARE @update_time DATETIME;
--		SET @update_time = (SELECT TOP 1 update_time FROM CEVAC_CACHE_RECORDS WHERE table_name = @name ORDER BY UTCDateTime DESC);
--		SET @where_subquery = ' WHERE UTCDateTime BETWEEN ' + CAST(@update_time AS NVARCHAR(50)) + ' AND ' + CAST(@now AS NVARCHAR(50));

		DECLARE @ExecSQL NVARCHAR(300);
		SET @ExecSQL = CONCAT('DROP TABLE ', @name_CACHE);
		EXEC(@ExecSQL);
	END

	SET @select_query = 'SELECT * INTO ' + @name_CACHE + ' FROM ' + @name
	-- + ' ' + isnull(@where_subquery, '');
	SELECT @select_query
	EXEC(@select_query);



	DECLARE @cache_query NVARCHAR(200);
	SET @cache_query = 'INSERT INTO CEVAC_CACHE_RECORDS(table_name, update_time) VALUES (''' + @name +''', ''' + CAST(@now AS nvarchar(50)) + ''')';

	SELECT @cache_query

	EXEC(@cache_query);

END
