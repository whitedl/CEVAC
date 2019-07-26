IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_CACHE_INIT') DROP PROCEDURE CEVAC_CACHE_INIT;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_CACHE_INIT
	@tables NVARCHAR(500),
	@destTableName NVARCHAR(300) = NULL
AS




DECLARE @name NVARCHAR(100);
DECLARE @name_CACHE NVARCHAR(100);
DECLARE @i INT;
DECLARE @params_rc INT;

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


SET @i = 100;
IF OBJECT_ID('dbo.#cevac_params', 'U') IS NOT NULL DROP TABLE #cevac_params;
SELECT * INTO #cevac_params FROM ListTable(@tables);
SET @params_rc = @@ROWCOUNT;
IF @params_rc > 1 AND @destTableName IS NOT NULL BEGIN
	RAISERROR('Custom init must have only one table', 11, 1);
	RETURN
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
	
	-- drop cache tables
	IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME=@name_CACHE) BEGIN
		DECLARE @ExecSQL NVARCHAR(MAX);
		SET @ExecSQL = CONCAT('DROP TABLE ', @name_CACHE);
		EXEC(@ExecSQL);
	END;



END
DECLARE @CEVAC_CACHE_APPEND NVARCHAR(MAX);

IF @tables LIKE '%HIST_LASR%' AND @params_rc = 1 BEGIN
	DECLARE @BuildingSName NVARCHAR(100);
	DECLARE @Metric NVARCHAR(100);
	SET @BuildingSName = (SELECT RTRIM(BuildingSName) FROM CEVAC_TABLES WHERE TableName = @tables);
	SET @Metric = (SELECT RTRIM(Metric) FROM CEVAC_TABLES WHERE TableName = @tables);

	SET @CEVAC_CACHE_APPEND = '
	IF OBJECT_ID(''CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST_LASR'') IS NOT NULL DROP TABLE CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST_LASR;
	EXEC CEVAC_VIEW @Building = ''' + @BuildingSName + ''', @Metric = ''' + @Metric + ''', @Age = ''HIST_LASR''';
END ELSE BEGIN
	SET @CEVAC_CACHE_APPEND = 'EXEC CEVAC_CACHE_APPEND @tables = ''' + @tables + '''';
END

EXEC(@CEVAC_CACHE_APPEND)