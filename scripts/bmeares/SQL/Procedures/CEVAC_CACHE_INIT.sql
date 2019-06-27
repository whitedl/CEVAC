IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_CACHE_INIT') DROP PROCEDURE CEVAC_CACHE_INIT;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_CACHE_INIT
	@tables NVARCHAR(500)
AS

DECLARE @name NVARCHAR(50);
DECLARE @name_CACHE NVARCHAR(50);
DECLARE @i INT;
SET @i = 100;
IF OBJECT_ID('dbo.#cevac_params', 'U') IS NOT NULL DROP TABLE #cevac_params;
SELECT * INTO #cevac_params FROM ListTable(@tables);
WHILE (EXISTS(SELECT 1 FROM #cevac_params) AND @i > 0) BEGIN
	SET @i = @i - 1;
	SET @name = (SELECT TOP 1 * FROM #cevac_params);
	DELETE TOP(1) FROM #cevac_params;


	-- Replace _VIEW with _CACHE, else append _CACHE
	SET @name_CACHE = REPLACE(@name, '_VIEW', '');
	SET @name_CACHE = @name_CACHE + '_CACHE';
--	SELECT @name_CACHE;

	
	-- drop cache tables
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME=@name_CACHE) BEGIN
		DECLARE @ExecSQL NVARCHAR(300);
		SET @ExecSQL = CONCAT('DROP TABLE ', @name_CACHE);
		EXEC(@ExecSQL);
	END;



END
DECLARE @CEVAC_CACHE_APPEND NVARCHAR(500);
SET @CEVAC_CACHE_APPEND = 'EXEC CEVAC_CACHE_APPEND @tables = ''' + @tables + '''';
SELECT @CEVAC_CACHE_APPEND;
EXEC(@CEVAC_CACHE_APPEND)