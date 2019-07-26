IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_QUORUM') DROP PROCEDURE CEVAC_QUORUM;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_QUORUM
	@BuildingSName NVARCHAR(200),
	@Metric NVARCHAR(100),
	@execute BIT = 1
AS

DECLARE @HIST NVARCHAR(500);
DECLARE @XREF NVARCHAR(500);
DECLARE @OLDEST NVARCHAR(500);
DECLARE @OLDEST_CACHE NVARCHAR(500);
DECLARE @LATEST_FULL NVARCHAR(500);
DECLARE @LATEST_FULL_CACHE NVARCHAR(500);
DECLARE @QUORUM NVARCHAR(500);
DECLARE @EXEC_SQL NVARCHAR(MAX);
DECLARE @DateTimeName NVARCHAR(100);
DECLARE @IDName NVARCHAR(100);
DECLARE @error NVARCHAR(MAX);

SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';
SET @XREF = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_XREF';
SET @QUORUM = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_QUORUM';
SET @OLDEST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_OLDEST';
SET @OLDEST_CACHE = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_OLDEST_CACHE';
SET @LATEST_FULL = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_LATEST_FULL';
SET @LATEST_FULL_CACHE = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_LATEST_FULL_CACHE';
SET @DateTimeName = RTRIM((SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE TableName = @HIST));
SET @IDName = RTRIM((SELECT TOP 1 IDName FROM CEVAC_TABLES WHERE TableName = @HIST));
IF @IDName IS NULL BEGIN
	SET @error = 'IDName is null';
	RAISERROR(@error,11,1);
	RETURN
END
IF @DateTimeName IS NULL BEGIN
	SET @error = 'DateTimeName is null';
	RAISERROR(@error,11,1);
	RETURN
END
IF @DateTimeName IS NULL BEGIN
	SET @error = 'DateTimeName is null';
	RAISERROR(@error,11,1);
	RETURN
END
-- Drop and recreate QUORUM

SET @EXEC_SQL = '
IF OBJECT_ID(''' + @QUORUM + ''') IS NOT NULL DROP TABLE ' + @QUORUM + ';
CREATE TABLE ' + @QUORUM + '(
	ReadingType NVARCHAR(100),
	begin_UTC DATETIME,
	end_UTC DATETIME,
	PSID_count INT
);
';
PRINT(@EXEC_SQL);
IF @execute = 1 EXEC(@EXEC_SQL);

SET @EXEC_SQL = '
DECLARE @begin DATETIME;
DECLARE @end DATETIME;
DECLARE @max_date DATETIME;
SET @max_date = CAST(''9999-12-31'' AS DATETIME);

DECLARE @oldest_times_type TABLE(UTCDateTime DATETIME);
DECLARE @types TABLE(Type NVARCHAR(100));
DECLARE @type NVARCHAR(100);
DECLARE @i INT;
DECLARE @j INT;

EXEC CEVAC_CACHE_INIT @tables = ''' + @OLDEST + ''';
EXEC CEVAC_CACHE_INIT @tables = ''' + @LATEST_FULL + ''';
INSERT INTO @types SELECT DISTINCT ReadingType FROM ' + @XREF + ';

SET @i = 10000;
WHILE EXISTS(SELECT TOP 1 * FROM @types) AND @i > 0 BEGIN
	SET @type = (SELECT TOP 1 Type FROM @types);
	DELETE TOP(1) FROM @types;
	SET @i = @i - 1;
	SET @j = 10000;

	DELETE FROM @oldest_times_type WHERE 1 = 1;
	INSERT INTO @oldest_times_type 
	SELECT o.' + @DateTimeName + ' FROM ' + @OLDEST_CACHE + ' AS o
	INNER JOIN ' + @XREF + ' AS x ON x.' + @IDName + ' = o.' + @IDName + '
	WHERE x.ReadingType = @type
	ORDER BY o.' + @DateTimeName + ' DESC;

	WHILE EXISTS(SELECT TOP 1 * FROM @oldest_times_type) AND @j > 0 BEGIN
	   	SET @begin = (SELECT TOP 1 ' + @DateTimeName + ' FROM @oldest_times_type);
		DELETE TOP(1) FROM @oldest_times_type;
		SET @end = (SELECT TOP 1 ' + @DateTimeName + ' FROM @oldest_times_type);
		SET @j = @j - 1;

		-- skip duplicate datetimes
		IF NOT EXISTS(SELECT * FROM @oldest_times_type WHERE ' + @DateTimeName + ' = @begin) BEGIN
			WITH type_points AS (
				SELECT o.' + @IDName + ', o.' + @DateTimeName + ' AS ''oldest_UTC'', l.' + @DateTimeName + ' AS ''latest_UTC''
				FROM ' + @XREF + ' AS x
				INNER JOIN ' + @OLDEST_CACHE + ' AS o ON x.' + @IDName + ' = o.' + @IDName + '
				INNER JOIN ' + @LATEST_FULL_CACHE + ' AS l ON x.' + @IDName + ' = l.' + @IDName + '
				WHERE x.ReadingType = @type
			)
			INSERT INTO ' + @QUORUM + '
			SELECT @type AS ''ReadingType'', @begin AS ''beginUTC'', ISNULL(@end,@max_date) AS ''endUTC'', COUNT(' + @IDName + ') AS ''PSID_count''
			FROM type_points
			WHERE oldest_UTC <= @begin 
			AND latest_UTC >= @begin
		END
	END
END
';

PRINT(@EXEC_SQL);
IF @execute = 1 EXEC(@EXEC_SQL);
