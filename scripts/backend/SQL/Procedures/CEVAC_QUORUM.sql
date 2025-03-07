IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_QUORUM') DROP PROCEDURE CEVAC_QUORUM;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_QUORUM
	@BuildingSName NVARCHAR(MAX),
	@Metric NVARCHAR(MAX),
	@types_list NVARCHAR(MAX),
	@execute BIT = 1
AS
DECLARE @error NVARCHAR(MAX);
DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);

DECLARE @HIST NVARCHAR(MAX);
DECLARE @XREF NVARCHAR(MAX);
DECLARE @OLDEST NVARCHAR(MAX);
DECLARE @OLDEST_CACHE NVARCHAR(MAX);
DECLARE @LATEST_FULL NVARCHAR(MAX);
DECLARE @LATEST_FULL_CACHE NVARCHAR(MAX);
DECLARE @QUORUM NVARCHAR(MAX);
DECLARE @EXEC_SQL NVARCHAR(MAX);
DECLARE @DateTimeName NVARCHAR(MAX);
DECLARE @IDName NVARCHAR(MAX);
DECLARE @agg_names TABLE(agg_name NVARCHAR(MAX));
DECLARE @now_str NVARCHAR(MAX);

SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';
SET @XREF = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_XREF';
SET @QUORUM = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_QUORUM';
SET @OLDEST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_OLDEST';
SET @OLDEST_CACHE = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_OLDEST_CACHE';
SET @LATEST_FULL = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_LATEST_FULL';
SET @LATEST_FULL_CACHE = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_LATEST_FULL_CACHE';
SET @DateTimeName = RTRIM((SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE TableName = @HIST));
SET @IDName = RTRIM((SELECT TOP 1 IDName FROM CEVAC_TABLES WHERE TableName = @HIST));
SET @now_str = CAST(GETUTCDATE() AS NVARCHAR(MAX));
EXEC CEVAC_ACTIVITY @TableName = @HIST, @ProcessName = @ProcessName;
INSERT INTO @agg_names SELECT * FROM ListTable(@types_list);
IF @IDName IS NULL BEGIN
	SET @error = 'IDName is null';
	EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @HIST;
	RAISERROR(@error,11,1);
	RETURN
END
IF @DateTimeName IS NULL BEGIN
	SET @error = 'DateTimeName is null';
	EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @HIST;
	RAISERROR(@error,11,1);
	RETURN
END
IF @DateTimeName IS NULL BEGIN
	SET @error = 'DateTimeName is null';
	EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @HIST;
	RAISERROR(@error,11,1);
	RETURN
END

-- Drop and recreate QUORUM
SET @EXEC_SQL = '
IF OBJECT_ID(''' + @QUORUM + ''') IS NOT NULL DROP TABLE ' + @QUORUM + ';
CREATE TABLE ' + @QUORUM + '(
	agg_name NVARCHAR(MAX),
	agg_key NVARCHAR(MAX),
	begin_UTC DATETIME,
	end_UTC DATETIME,
	PSID_count INT,
	debug_PSID_count INT,
	artificial_PSID INT
);
EXEC CEVAC_CACHE_INIT @tables = ''' + @OLDEST + ''';
EXEC CEVAC_CACHE_INIT @tables = ''' + @LATEST_FULL + ''';
';
PRINT(@EXEC_SQL);
IF @execute = 1 EXEC(@EXEC_SQL);

DECLARE @i INT;
SET @i = 100;
DECLARE @agg_name NVARCHAR(MAX);

WHILE EXISTS(SELECT TOP 1 * FROM @agg_names) AND @i > 0 BEGIN
	SET @agg_name = (SELECT TOP 1 agg_name FROM @agg_names ORDER BY agg_name DESC); -- DEBUG change to ASC
	WITH del AS (SELECT TOP 1 * FROM @agg_names ORDER BY agg_name DESC) DELETE FROM del;
--	DELETE TOP(1) FROM @agg_names;
	SET @i = @i + 1;

	SET @EXEC_SQL = '
	DECLARE @begin DATETIME;
	DECLARE @is_birth BIT;
	DECLARE @count INT;
	DECLARE @end DATETIME;
	DECLARE @max_date DATETIME;
	SET @max_date = CAST(''9999-12-31'' AS DATETIME);

	DECLARE @oldest_times_type TABLE(' + @DateTimeName + ' DATETIME);
	DECLARE @newest_times_type TABLE(' + @DateTimeName + ' DATETIME);
	DECLARE @all_times_type TABLE(' + @DateTimeName + ' DATETIME, is_birth BIT, count INT);
	DECLARE @types TABLE(Type NVARCHAR(MAX));
	DECLARE @Readingtypes TABLE(ReadingType NVARCHAR(100));
--	DECLARE @Floors TABLE(Floor NVARCHAR(100));
	DECLARE @type NVARCHAR(100);
	DECLARE @i INT;
	DECLARE @j INT;
	DECLARE @PSID_loop_count INT;
	DECLARE @artificial_PSID INT;

	INSERT INTO @types SELECT DISTINCT ' + @agg_name + ' AS ''Type'' FROM ' + @XREF + ';
	DECLARE @PSIDCount INT;
	SET @i = 100;
--	SELECT * FROM @types;
	WHILE EXISTS(SELECT TOP 1 * FROM @types) AND @i > 0 BEGIN
		SET @type = (SELECT TOP 1 Type FROM @types ORDER BY Type DESC);
--		SELECT @type AS ''DEBUG TYPE'';
		WITH del AS (SELECT TOP 1 * FROM @types ORDER BY Type DESC) DELETE FROM del;
		SET @PSIDCount = (SELECT COUNT(*) FROM ' + @XREF + ' WHERE ' + @agg_name + ' = @type AND ' + @IDName + ' < 0);
--		IF @PSIDCount > 0 CONTINUE;

		SET @artificial_PSID = (SELECT TOP 1 ' + @IDName + ' FROM ' + @XREF + ' WHERE ' + @agg_name + ' = @type AND ' + @IDName + ' < 0);
		SET @i = @i - 1;
		
		DELETE FROM @oldest_times_type WHERE 1 = 1;
		DELETE FROM @newest_times_type WHERE 1 = 1;
		DELETE FROM @all_times_type WHERE 1 = 1;

		INSERT INTO @oldest_times_type 
			SELECT o.' + @DateTimeName + ' FROM ' + @OLDEST_CACHE + ' AS o
			INNER JOIN ' + @XREF + ' AS x ON x.' + @IDName + ' = o.' + @IDName + '
			WHERE x.' + @agg_name + ' = @type
			ORDER BY o.' + @DateTimeName + ' DESC;

		INSERT INTO @newest_times_type 
			SELECT o.' + @DateTimeName + ' FROM ' + @LATEST_FULL_CACHE + ' AS o
			INNER JOIN ' + @XREF + ' AS x ON x.' + @IDName + ' = o.' + @IDName + '
			WHERE x.' + @agg_name + ' = @type
			ORDER BY o.' + @DateTimeName + ' DESC;
	
		DELETE FROM @newest_times_type
			WHERE ' + @DateTimeName + ' > DATEADD(DAY, -7, ''' + @now_str + ''');

		INSERT INTO @all_times_type
			SELECT DISTINCT ' + @DateTimeName + ', ''1'' AS is_birth, COUNT(' + @DateTimeName + ') AS count
			FROM @oldest_times_type
			GROUP BY ' + @DateTimeName + '
			UNION
			SELECT DISTINCT ' + @DateTimeName + ', ''0'' AS is_birth, COUNT(' + @DateTimeName + ') AS count
			FROM @newest_times_type
			GROUP BY ' + @DateTimeName + ';

		SELECT @type AS ''type'';
		SELECT * FROM @all_times_type;
		SELECT * FROM @newest_times_type;
		SELECT * FROM @oldest_times_type;
		
		-----------------------
		-- Loop through all birth and death datetimes (OLDEST and LATEST_FULL) by type
		-- Set begin to first and end to second (define a period)
		-- Last one will be NULL (replaced with @max_date)
		-----------------------
		SET @j = 100;
		SET @PSID_loop_count = 0;
		WHILE EXISTS(SELECT TOP 1 * FROM @all_times_type) AND @j > 0 BEGIN
	   		SET @begin = (SELECT TOP 1 ' + @DateTimeName + ' FROM @all_times_type ORDER BY ' + @DateTimeName + ' ASC);
			SET @count = (SELECT TOP 1 count FROM @all_times_type ORDER BY ' + @DateTimeName + ' ASC);
			SET @is_birth = (SELECT TOP 1 is_birth FROM @all_times_type ORDER BY ' + @DateTimeName + ' ASC);
			IF @is_birth = 1 SET @PSID_loop_count = @PSID_loop_count + @count;
			ELSE SET @PSID_loop_count = @PSID_loop_count - @count;
			WITH del AS (SELECT TOP 1 * FROM @all_times_type ORDER BY ' + @DateTimeName + ' ASC) DELETE FROM del;
--			DELETE TOP(1) FROM @all_times_type WHERE ' + @DateTimeName + ' = @begin;
			SET @end = (SELECT TOP 1 ' + @DateTimeName + ' FROM @all_times_type WHERE ' + @DateTimeName + ' > @begin ORDER BY ' + @DateTimeName + ' ASC);
			SET @j = @j - 1;
		
			-- skip duplicate datetimes
			IF NOT EXISTS(SELECT * FROM ' + @QUORUM + ' WHERE begin_UTC = @begin AND agg_key = @type) BEGIN
				---------
				-- TWO METHODS OF CALCULATING PSID_count:
				-- (1)  Vertical line test:
				--		Only count points whose births precede / equal the @begin time and whose deaths exceed / equal the @end time
				--		(enforced via the below WHERE clause)
				-- (2)  Running total:
				--		Iterate through all births and deaths (in order) and increment / decrement a counter by the frequency (@count) of births / deaths.
				-- Note: PSID_count is implemented below via method (1). debug_PSID_count is calculated via method (2) as a way to verify PSID_count.
				---------
				IF @type = ''Building'' BEGIN
					SELECT @begin AS ''begin'';
					SELECT @end AS ''end'';
				END;
				WITH type_points AS (
					SELECT o.' + @IDName + ', o.' + @DateTimeName + ' AS ''oldest_UTC'', l.' + @DateTimeName + ' AS ''latest_UTC''
					FROM ' + @XREF + ' AS x
					INNER JOIN ' + @OLDEST_CACHE + ' AS o ON x.' + @IDName + ' = o.' + @IDName + '
					INNER JOIN ' + @LATEST_FULL_CACHE + ' AS l ON x.' + @IDName + ' = l.' + @IDName + '
					WHERE x.' + @agg_name + ' = @type
				)
				INSERT INTO ' + @QUORUM + '
				SELECT ''' + @agg_name + ''' AS ''agg_name'', @type AS ''agg_key'', @begin AS ''beginUTC'', ISNULL(@end,@max_date) AS ''endUTC'', COUNT(' + @IDName + ') AS ''PSID_count'', @PSID_loop_count AS ''debug_PSID_count'', @artificial_PSID AS ''artificial_PSID''
				FROM type_points
				WHERE oldest_UTC <= @begin 
				AND latest_UTC > @begin
			END
		END
	END
	';

	PRINT(@EXEC_SQL);
	IF @execute = 1 EXEC(@EXEC_SQL);


END
