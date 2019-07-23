IF OBJECT_ID('CEVAC_SP_AGG_ALL') IS NOT NULL DROP PROCEDURE CEVAC_SP_AGG_ALL;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_SP_AGG_ALL(
	@BuildingSName NVARCHAR(100),
	@Metric NVARCHAR(100))

AS
BEGIN
DECLARE @execute BIT;
SET @execute = 1;

DECLARE @HIST NVARCHAR(300);
DECLARE @HIST_LASR NVARCHAR(300);
DECLARE @HIST_LASR_INT NVARCHAR(300); -- itermediate table (for caching)
DECLARE @XREF NVARCHAR(300);
DECLARE @sp_aliases NVARCHAR(350);
DECLARE @filtered NVARCHAR(350);
DECLARE @DateTimeName NVARCHAR(100);
DECLARE @AliasName NVARCHAR(100);
DECLARE @DataName NVARCHAR(100);
DECLARE @now_UTC_string NVARCHAR(100);

SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';
SET @HIST_LASR = @HIST + '_LASR';
SET @HIST_LASR_INT = @HIST_LASR + '_INT';
SET @XREF = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_XREF';
SET @sp_aliases = '#' + @HIST + '_sp_aliases';
SET @filtered = '#' + @HIST + '_filtered';
SET @DateTimeName = (SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE TableName = @HIST);
SET @AliasName = (SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE TableName = @HIST);
SET @DataName = (SELECT TOP 1 RTRIM(DataName) FROM CEVAC_TABLES WHERE TableName = @HIST);
SET @now_UTC_string = CAST(GETUTCDATE() AS NVARCHAR(100));

--DECLARE @drop_lasr NVARCHAR(MAX);
--SET @drop_lasr = '
--IF OBJECT_ID(''' + @HIST_LASR + ''') IS NOT NULL DROP TABLE ' + @HIST_LASR + ';
--';

--PRINT @drop_lasr;
--IF @execute = 1 EXEC(@drop_lasr);

-- Create empty table with identical structure
DECLARE @create_lasr NVARCHAR(MAX);
SET @create_lasr = '
IF OBJECT_ID(''' + @HIST_LASR_INT + ''') IS NOT NULL DROP TABLE ' + @HIST_LASR_INT + ';
SELECT * INTO ' + @HIST_LASR_INT + ' FROM ' + @HIST + ' WHERE 1 = 2;
';
-- IF OBJECT_ID(''' + @HIST_LASR + ''') IS NULL SELECT * INTO ' + @HIST_LASR + ' FROM ' + @HIST + ' WHERE 1 = 2;

PRINT @create_lasr;
IF @execute = 1 EXEC(@create_lasr);

DECLARE @EXEC_SQL NVARCHAR(MAX);

SET @EXEC_SQL = '
IF OBJECT_ID(''' + @sp_aliases + ''') IS NOT NULL DROP TABLE ' + @sp_aliases + ';
SELECT DISTINCT ' + @AliasName + ' INTO ' + @sp_aliases + ' FROM ' + @XREF + ' WHERE ReadingType LIKE ''%SP%'';

DECLARE @last_UTC DATETIME;
IF OBJECT_ID(''' + @HIST_LASR + ''') IS NOT NULL BEGIN
	SET @last_UTC = ISNULL((SELECT TOP 1 ' + @DateTimeName + ' FROM ' + @HIST_LASR + ' ORDER BY ' + @DateTimeName + ' DESC),CAST(0 AS DATETIME));
END ELSE SET @last_UTC = CAST(0 AS DATETIME);
DECLARE @begin_UTC_string_orig NVARCHAR(100);
IF @last_UTC > 0 SET @begin_UTC_string_orig = CAST(DATEADD(DAY, -7, @last_UTC) AS NVARCHAR(100))
ELSE SET @begin_UTC_string_orig = CAST(@last_UTC AS NVARCHAR(100));

DECLARE @loop_alias NVARCHAR(100);
DECLARE @i INT;
SET @i = 1;

DECLARE @count INT;
SET @count = (SELECT COUNT(*) AS c FROM ' + @sp_aliases + ');
PRINT ''COUNT IS: '' + CAST(@count AS NVARCHAR(20));

WHILE EXISTS (SELECT TOP 1 * FROM ' + @sp_aliases + ') AND @i < 501 BEGIN
	SET @loop_alias = (SELECT TOP 1 ' + @AliasName + ' FROM ' + @sp_aliases + ');
	DELETE TOP (1) FROM ' + @sp_aliases + ';
	PRINT CAST((@count - @i) AS NVARCHAR(20)) + '' remaining'';
	SET @i = @i + 1;

	INSERT INTO ' + @HIST_LASR_INT + ' 
	EXEC CEVAC_SP_AGG @Alias = @loop_alias, @HIST = ''' + @HIST + ''', @begin_UTC_string = @begin_UTC_string_orig, @now_UTC_string = ''' + @now_UTC_string + ''', @DateTimeName = ''' + @DateTimeName + ''', @AliasName = ''' + @AliasName + ''', @DataName = ''' + @DataName + ''';
END

DECLARE @setback_UTC DATETIME;
IF @last_UTC > 0 SET @setback_UTC = DATEADD(DAY, -3, @last_UTC)
ELSE SET @setback_UTC = @last_UTC;
IF OBJECT_ID(''' + @HIST_LASR + ''') IS NOT NULL BEGIN
	DELETE FROM ' + @HIST_LASR + '
	WHERE ' + @DateTimeName + ' > @setback_UTC;
END

DECLARE @now_UTC DATETIME;
SET @now_UTC = CAST(''' + @now_UTC_string + ''' AS DATETIME);
DECLARE @begin_UTC DATETIME;
SET @begin_UTC = DATEADD(MONTH, -1, @last_UTC);

INSERT INTO ' + @HIST_LASR_INT + ' 
SELECT * FROM ' + @HIST + '
WHERE ' + @AliasName + ' NOT LIKE ''%SP%''
AND ' + @DataName + ' BETWEEN @begin_UTC AND @now_UTC;
';
PRINT @EXEC_SQL;
IF @execute = 1 EXEC(@EXEC_SQL);

DECLARE @cache_append_query NVARCHAR(MAX);
SET @cache_append_query = '
EXEC CEVAC_CACHE_APPEND @tables = ''' + @HIST_LASR_INT + ''', @destTableName = ''' + @HIST_LASR + ''';
';
PRINT @cache_append_query;
IF @execute = 1 EXEC(@cache_append_query);

END

