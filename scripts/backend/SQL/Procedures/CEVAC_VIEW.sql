IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_VIEW') DROP PROCEDURE CEVAC_VIEW;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_VIEW
	@Building NVARCHAR(30),
	@Metric NVARCHAR(30),
	@Age NVARCHAR(30),
	@keys_list NVARCHAR(500) = '',
	@unitOfMeasureID int = NULL,
	@execute BIT = 1
	

AS

DECLARE @error NVARCHAR(MAX);
DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);

DECLARE @cevac_config_temp TABLE(
	VarName NVARCHAR(MAX),
	VarValue NVARCHAR(MAX)
);
INSERT INTO @cevac_config_temp SELECT * FROM CEVAC_CONFIG;

DECLARE @RemoteIP NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteIP'),
	@RemoteDB NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteDB'),
	@RemoteSchema NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteSchema'),
	@RemoteAVTable NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteAVTable'),
	@RemoteUnitTable NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteUnitTable'),
	@RemotePSTable NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemotePSTable'),
	@RemotePtTable NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemotePtTable'),
	@RemoteUTCName NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteUTCName'),
	@RemotePSIDName NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemotePSIDName'),
	@RemotePointIDName NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemotePointIDName'),
	@RemoteUnitOfMeasureIDName NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteUnitOfMeasureIDName'),
	@RemotePointNameName NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemotePointNameName'),
	@RemoteActualValueName NVARCHAR(MAX) = (SELECT TOP 1 VarValue FROM @cevac_config_temp WHERE VarName = 'RemoteActualValueName')
	;

DECLARE @building_key NVARCHAR(MAX);
--SET @execute = 1;

SET @building_key = (SELECT RTRIM(BuildingKey) FROM CEVAC_BUILDING_INFO WHERE BuildingSName = @Building);
--IF @building_key IS NULL BEGIN
--	RAISERROR('Add BuildingSName to CEVAC_BUILDING_INFO', 0, 1);
--	RETURN
--END

DECLARE @Table_name NVARCHAR(MAX);
DECLARE @HIST_VIEW NVARCHAR(MAX);
DECLARE @HIST_CACHE NVARCHAR(MAX);
DECLARE @HIST_LASR NVARCHAR(MAX);
DECLARE @HIST_LASR_INT NVARCHAR(MAX);
DECLARE @HIST NVARCHAR(MAX);
DECLARE @DAY NVARCHAR(MAX);
DECLARE @LATEST NVARCHAR(MAX);
DECLARE @LATEST_FULL NVARCHAR(MAX);
DECLARE @LATEST_BROKEN NVARCHAR(MAX);
DECLARE @OLDEST NVARCHAR(MAX);
DECLARE @XREF NVARCHAR(MAX);
DECLARE @PXREF NVARCHAR(MAX);
DECLARE @TABLE_CONFIG NVARCHAR(MAX);

-- Generate table names
-- Reference names
SET @HIST_VIEW = 'CEVAC_' + @Building + '_' + @Metric + '_HIST_VIEW';
SET @HIST_CACHE = 'CEVAC_' + @Building + '_' + @Metric + '_HIST_CACHE';
SET @HIST_LASR = 'CEVAC_' + @Building + '_' + @Metric + '_HIST_LASR';
SET @HIST_LASR_INT = 'CEVAC_' + @Building + '_' + @Metric + '_HIST_LASR_INT';
SET @HIST = 'CEVAC_' + @Building + '_' + @Metric + '_HIST';
SET @DAY = 'CEVAC_' + @Building + '_' + @Metric + '_DAY';
SET @LATEST = 'CEVAC_' + @Building + '_' + @Metric + '_LATEST';
SET @LATEST_FULL = 'CEVAC_' + @Building + '_' + @Metric + '_LATEST_FULL';
SET @LATEST_BROKEN = 'CEVAC_' + @Building + '_' + @Metric + '_LATEST_BROKEN';
SET @OLDEST = 'CEVAC_' + @Building + '_' + @Metric + '_OLDEST';


-- Current name
IF @Age = 'HIST' SET @Table_name = CONCAT('CEVAC_', @Building, '_', @Metric, '_', @Age, '_VIEW')
ELSE SET @Table_name = CONCAT('CEVAC_', @Building, '_', @Metric, '_', @Age);
PRINT @Table_name;
SET @XREF = CONCAT('CEVAC_', @Building, '_', @Metric, '_XREF');
IF @Metric = 'POWER_SUMS' SET @XREF = CONCAT('CEVAC_', @Building, '_POWER_XREF');
SET @PXREF = CONCAT('CEVAC_', @Building, '_', @Metric, '_PXREF');
--IF @Metric = 'POWER_RAW' SET @XREF = CONCAT('CEVAC_', @Building, '_', REPLACE(@Metric, 'POWER_RAW', 'POWER'), '_XREF');
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF) SET @XREF = NULL;

SET @TABLE_CONFIG = @Table_name + '_CONFIG';
DECLARE @Create_TABLE_CONFIG NVARCHAR(MAX);
SET @Create_TABLE_CONFIG = '
IF OBJECT_ID(''' + @TABLE_CONFIG + ''') IS NOT NULL DROP TABLE ' + @TABLE_CONFIG + '
SELECT TOP 1 * INTO ' + @TABLE_CONFIG + ' FROM CEVAC_TABLES WHERE TableName = ''' + @Table_name + '''
';

DECLARE @Dependencies_list NVARCHAR(MAX);
-- Verify all dependencies (runs only if table is in CEVAC_TABLES)
IF EXISTS (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @Table_name) BEGIN
	
	DECLARE @Dependencies_query NVARCHAR(MAX);
	SET @Dependencies_query = '';
	DECLARE @dependency NVARCHAR(200);
	DECLARE @dependency_query NVARCHAR(500);
	SET @Dependencies_list = (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @Table_name);
	IF @Dependencies_list IS NOT NULL BEGIN
		DECLARE @cevac_dep TABLE(dep NVARCHAR(MAX));
		INSERT INTO @cevac_dep SELECT * FROM ListTable(@Dependencies_list);
		DECLARE @i INT;
		SET @i = 100;
		WHILE (EXISTS(SELECT 1 FROM @cevac_dep) AND @i > 0) BEGIN
			SET @dependency = (SELECT TOP 1 * FROM @cevac_dep);
			DELETE TOP(1) FROM @cevac_dep;
			SET @dependency_query = '
			IF OBJECT_ID(''' + @dependency + ''') IS NULL BEGIN
				EXEC CEVAC_LOG_ERROR @ErrorMessage = ''' + @Table_name + ' requires ' + @dependency + ''', @ProcessName = ''' + @ProcessName + ''', @TableName = ''' + @Table_name + ''';
				RAISERROR(''' + @Table_name + ' requires ' + @dependency + ''', 11, 1);
				RETURN
			END
			';

			SET @Dependencies_query = @Dependencies_query + @dependency_query;

			SET @i = @i - 1;
		END
		IF @execute = 1 EXEC(@Dependencies_query);
	END -- end of Dependencies verifications
END

-- Drop view for rebuilding
IF OBJECT_ID(@Table_name, 'V') IS NOT NULL BEGIN
	DECLARE @DropView NVARCHAR(500);
	SET @DropView = 'DROP VIEW ' + @Table_name;
	EXEC(@DropView);
END

-- Build subqueries 
DECLARE @keys_list_query NVARCHAR(500);
SET @keys_list_query = ' INNER JOIN ListTable(''' + @keys_list + ''') AS Params ON pt.PointName LIKE ''%'' + Params.items + ''%''';

IF @unitOfMeasureID IS NULL AND @Metric IN (SELECT Metric FROM CEVAC_METRIC) BEGIN
	SET @unitOfMeasureID = (SELECT TOP 1 unitOfMeasureID FROM CEVAC_METRIC WHERE Metric = @Metric);
END


DECLARE @XREF_query NVARCHAR(500);
DECLARE @Alias_or_PSID NVARCHAR(100);
SET @Alias_or_PSID = 'Alias';
DECLARE @DateTimeName NVARCHAR(100);
DECLARE @AliasName NVARCHAR(100);
DECLARE @IDName NVARCHAR(100);
DECLARE @DataName NVARCHAR(100);
DECLARE @isCustom BIT;
DECLARE @customLASR BIT;
DECLARE @autoCACHE BIT;
DECLARE @autoLASR BIT;
DECLARE @XREF_or_PXREF NVARCHAR(100);
DECLARE @CEVAC_TABLES_config TABLE(COLUMN_NAME NVARCHAR(200), COLUMN_VALUE NVARCHAR(200));
INSERT INTO @CEVAC_TABLES_config SELECT COLUMN_NAME, NULL AS COLUMN_VALUE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'CEVAC_TABLES';


SET @customLASR = 0;  -- DEFAULT
SET @autoCACHE = 0;   -- DEFAULT
SET @autoLASR = 0;    -- DEFAULT
SET @XREF_or_PXREF = 'XREF'; -- DEFAULT

-- If XREF doesn't exist, select PointSliceID instead
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF)
BEGIN
	SET @XREF_or_PXREF = 'PXREF';
	SET @XREF_query = 'INNER JOIN ' + @PXREF + ' AS xref on xref.' + @RemotePSIDName + ' = val.' + @RemotePSIDName + '';
	SET @Alias_or_PSID = @RemotePSIDName;
END ELSE IF @Age = 'HIST' BEGIN -- XREF exists
	-- Insert XREF into CEVAC_TABLES
	PRINT 'Adding XREF to table: ' + @XREF;
	IF @execute = 1 BEGIN
		-- Check if XREF contains setpoints. If so, flip customLASR (for CEVAC_HIST_LASR)
		DECLARE @customLASR_query NVARCHAR(MAX);
		DECLARE @customLASR_rc INT;
		IF 'ReadingType' IN (SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = @XREF) BEGIN
			SET @customLASR_query = 'SELECT TOP 1 * FROM ' + @XREF + ' WHERE ReadingType LIKE ''%SP%''';
			EXEC(@customLASR_query);
			SET @customLASR_rc = @@ROWCOUNT;
			IF @customLASR_rc > 0 SET @customLASR = 1;
		END
		
		DELETE FROM CEVAC_TABLES WHERE TableName = @XREF;
		INSERT INTO CEVAC_TABLES(BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, customLASR)
		VALUES (@Building, @Metric, 'XREF', @XREF, @RemotePSIDName, @RemotePSIDName, 'Alias', @RemotePSIDName, @customLASR);
	END
END

SET @DateTimeName = @RemoteUTCName; -- DEFAULT
SET @AliasName = 'Alias';   -- DEFAULT
SET @IDName = @RemotePSIDName; -- DEFAULT
SET @DataName = @RemoteActualValueName;     -- DEFAULT
SET @isCustom = 0;                 -- DEFAULT
-------------------------------------------------------
-- There exists a similar table within CEVAC_TABLES
-- Grab AliasName, DateTimeName, and isCustom from HIST
-------------------------------------------------------
IF @Age != 'XREF' AND EXISTS (SELECT TOP 1 * FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age NOT LIKE '%XREF%') BEGIN
	SET @DateTimeName = RTRIM((SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'));
	SET @IDName = RTRIM((SELECT TOP 1 IDName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'));
	SET @AliasName = RTRIM((SELECT TOP 1 AliasName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'));
	SET @DataName = RTRIM((SELECT TOP 1 DataName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'));
	SET @isCustom = (SELECT TOP 1 isCustom FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST');

	DECLARE @loop TABLE(VALUE NVARCHAR(200));
	INSERT INTO @loop SELECT COLUMN_NAME FROM @CEVAC_TABLES_config;

	DECLARE @col_name NVARCHAR(200);
	WHILE EXISTS(SELECT TOP 1 * FROM @loop) BEGIN
		SET @col_name = (SELECT TOP 1 VALUE FROM @loop);	
		DELETE TOP(1) FROM @loop;
		UPDATE @CEVAC_TABLES_config SET COLUMN_VALUE = 'test' WHERE COLUMN_NAME = @col_name;
	END -- end loop

END

SET @DataName = ISNULL(@DataName,@RemoteActualValueName);     -- DEFAULT
SET @IDName = ISNULL(@IDName,@RemotePSIDName);   -- DEFAULT
SET @AliasName = ISNULL(@AliasName,'Alias');   -- DEFAULT
SET @DateTimeName = ISNULL(@DateTimeName,@RemoteUTCName);   -- DEFAULT

-- build view query
DECLARE @Create_View nvarchar(MAX);


--------------------------------
-- Verify everything is in order
--------------------------------
IF @Age LIKE 'HIST' AND @isCustom = 0 BEGIN
	IF OBJECT_ID(@XREF) IS NULL AND OBJECT_ID(@PXREF) IS NULL AND @building_key IS NOT NULL BEGIN
		SET @error = @HIST + ' requires ' + @XREF + ' or ' + @PXREF;
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error, 11, 1);
		RETURN
	END
END
IF @Age LIKE 'DAY' BEGIN
	IF OBJECT_ID(@HIST) IS NULL BEGIN
		SET @error = @DAY + ' requires ' + @HIST;
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error, 11, 1);
		RETURN
	END
END
IF @Age LIKE 'LATEST%' BEGIN
	IF OBJECT_ID(@DAY) IS NULL OR OBJECT_ID(@HIST) IS NULL BEGIN
		SET @error = @LATEST + ' requires ' + @HIST + ' and ' + @DAY;
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error, 11, 1);
		RETURN
	END
END
IF @Age LIKE 'OLDEST%' BEGIN
	IF OBJECT_ID(@HIST) IS NULL BEGIN
		SET @error = @OLDEST + ' requires ' + @HIST;
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error, 11, 1);
		RETURN
	END
END
IF @Age LIKE 'LATEST_BROKEN' BEGIN
	IF OBJECT_ID(@DAY) IS NULL OR OBJECT_ID(@HIST) IS NULL OR OBJECT_ID(@LATEST) IS NULL OR OBJECT_ID(@LATEST_FULL) IS NULL BEGIN
		SET @error = @LATEST_BROKEN + ' requires ' + @LATEST + ', ' + @LATEST_FULL + ', ' + @DAY + ', and ' + @HIST;
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error, 11, 1);
		RETURN
	END
END



-----------------------------------------------
-- Age: PXREF (standard)
--
-- Requires:
-- None (init standard bootstrap with PXREF)
-----------------------------------------------
IF @Age LIKE '%PXREF%' BEGIN
	DECLARE @unitOfMeasureID_query NVARCHAR(1000);
	IF @unitOfMeasureID IS NOT NULL BEGIN
		SET @unitOfMeasureID_query = ' units.' + @RemoteUnitOfMeasureIDName + ' = ' + CAST(ISNULL(@unitOfMeasureID,-1) AS NVARCHAR(100));
	END
		
	IF @building_key IS NULL BEGIN
		SET @error = 'Missing building key. Check CEVAC_BUILDING_INFO if ' + @Building + ' exists';
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error,11,1);
		RETURN
	END
	IF @PXREF IS NULL BEGIN
		SET @error = 'Error: PXREF variable is null';
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error,11,1);
		RETURN
	END
	DECLARE @PXREF_query NVARCHAR(MAX);
	IF @keys_list_query IS NULL BEGIN
		SET @error = 'Error: Keys list query is null';
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error,11,1);
		RETURN
	END

	DELETE FROM CEVAC_TABLES WHERE TableName = @PXREF;

	DECLARE @PXREF_Alias_source NVARCHAR(MAX);
	DECLARE @PXREF_Alias_join NVARCHAR(MAX);
	IF OBJECT_ID(@XREF) IS NULL BEGIN
		SET @PXREF_Alias_source = @RemotePointNameName;
		SET @PXREF_Alias_join = NULL;
	END ELSE BEGIN
		SET @PXREF_Alias_source = 'xref.Alias';
		SET @PXREF_Alias_join = 'INNER JOIN ' + @XREF + ' AS xref ON xref.' + @RemotePSIDName + ' = ps.' + @RemotePSIDName;
	END

	SET @PXREF_query = '
		IF OBJECT_ID(''dbo.' + @PXREF + ''', ''U'') IS NOT NULL DROP TABLE ' + @PXREF + ';
		SELECT DISTINCT
			ps.' + @RemotePSIDName + ', pt.' + @RemotePointNameName + ', ' + @PXREF_Alias_source + ' AS ''Alias'', units.' + @RemoteUnitOfMeasureIDName + '
		INTO ' + @PXREF + '
		FROM
			[' + @RemoteIP + '].' + @RemoteDB + '.' + @RemoteSchema + '.' + @RemotePtTable + ' AS pt
			INNER JOIN [' + @RemoteIP + '].' + @RemoteDB + '.' + @RemoteSchema + '.' + @RemotePSTable + ' AS ps ON pt.' + @RemotePointIDName + ' = ps.' + @RemotePointIDName + ' 
			INNER JOIN [' + @RemoteIP + '].' + @RemoteDB + '.' + @RemoteSchema + '.' + @RemoteUnitTable + ' AS units ON units.' + @RemoteUnitOfMeasureIDName + ' = pt.' + @RemoteUnitOfMeasureIDName + '
			' + ISNULL(@PXREF_Alias_join, '') + '
			' + @keys_list_query + '
		WHERE
		( pt.' + @RemotePointNameName + ' LIKE ''' + @building_key + ''')
		AND ' + ISNULL(@unitOfMeasureID_query, '1 = 1') + '
		';
	PRINT @PXREF_query;
	IF @execute = 1 BEGIN
		EXEC(@PXREF_query);
		DELETE FROM CEVAC_TABLES WHERE TableName = @PXREF;
		INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Definition, Dependencies, customLASR, autoCACHE, autoLASR)
		VALUES (
			@Building,
			@Metric,
			@Age,
			@PXREF,
			@RemotePSIDName,
			@RemotePSIDName,
			'Alias',
			@RemotePSIDName,
			@isCustom,
			@PXREF_query,
			NULL,
			isnull(@customLASR,0),
			isnull(@autoCACHE,0),
			isnull(@autoLASR,0)
		)
		
	END
END


------------------------------------------------------------
-- Age: HIST_VIEW (standard)
--
-- Requires:
-- XREF or PXREF (only if standard)
-- Note: Dependencies left NULL for non-standard HIST tables
------------------------------------------------------------
ELSE IF @Age LIKE '%HIST%' BEGIN

	DECLARE @xref_source NVARCHAR(300);
	IF @XREF_or_PXREF = 'XREF' SET @xref_source = @XREF;
	ELSE IF @XREF_or_PXREF = 'PXREF' SET @xref_source = @PXREF;
	ELSE BEGIN
		SET @error = 'Could not distinguish XREF source';
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error,11,1);
		RETURN
	END

	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS

	SELECT xref.' + @RemotePSIDName + ', xref.Alias AS Alias, val.' + @RemoteUTCName + ', dbo.ConvertUTCToLocal(val.' + @RemoteUTCName + ') AS ETDateTime, val.' + @RemoteActualValueName + ' 
	FROM
		[' + @RemoteIP + '].' + @RemoteDB + '.' + @RemoteSchema + '.' + @RemoteAVTable + ' AS val
	INNER JOIN ' + @xref_source + ' as xref ON xref.' + @RemotePSIDName + ' = val.' + @RemotePSIDName + '
	';

	IF @Age LIKE '%LASR%' BEGIN
		SET @Create_View = '
		EXEC CEVAC_HIST_LASR @BuildingSName = ''' + @Building + ''', @Metric = ''' + @Metric + ''';
		';
		SET @customLASR = 1;
		SET @Table_name = @HIST_LASR;
	END
	SET @autoCACHE = 1;
	SET @autoLASR = 0;

END -- END of HIST_VIEW
		
-----------------------------------------------
-- Age: DAY
--
-- Requires:
-- HIST
-----------------------------------------------
ELSE IF @Age = 'DAY' BEGIN
	SET @Dependencies_list = @HIST;
	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS
	SELECT * FROM ' + @HIST + '
	WHERE ' + @DateTimeName + ' <= GETUTCDATE() AND ' + @DateTimeName + ' >= DATEADD(day, -1, GETUTCDATE())
	';
	SET @autoCACHE = 0;
	SET @autoLASR = 0;
END	 -- END of DAY

-----------------------------------------------
-- Age: MONTH
--
-- Requires:
-- HIST
-----------------------------------------------
ELSE IF @Age = 'MONTH' BEGIN
	SET @Dependencies_list = @HIST;
	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS
	SELECT * FROM ' + @HIST + '
	WHERE ' + @DateTimeName + ' <= GETUTCDATE() AND ' + @DateTimeName + ' >= DATEADD(MONTH, -1, GETUTCDATE())
	';
	SET @autoCACHE = 0;
	SET @autoLASR = 0;
END	 -- END of MONTH

-----------------------------------------------
-- Ages: LATEST, LATEST_FULL, and LATEST_BROKEN
--
-- Requires:
-- HIST, DAY
-- LATEST, LATEST_FULL (for LATEST_BROKEN)
-----------------------------------------------
ELSE IF @Age LIKE '%LATEST%' BEGIN
	SET @Dependencies_list = @HIST + ',' + @DAY;
	DECLARE @Latest_source NVARCHAR(500);
	IF @Age LIKE '%FULL%' SET @Latest_source = @HIST;
	ELSE SET @Latest_source = @DAY;
	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS
	SELECT ' +
	' temp.* FROM '  + @Latest_source + ' AS temp
	INNER JOIN
	(
		SELECT ' + @IDName + ', 
		MAX(' + @DateTimeName + ') AS LastTime
		FROM
		' + @Latest_source + '
		GROUP BY ' + @IDName + '
	) AS recent
	ON
	temp.' + @IDName + ' = recent.' + @IDName + '
	AND temp.' + @DateTimeName + ' = recent.LastTime
	';
	SET @autoLASR = 1;
	SET @autoCACHE = 0;

	-- NOTE: LATEST and LATEST_FULL must exist
	IF @Age LIKE '%BROKEN%' BEGIN
		SET @Dependencies_list = @HIST + ',' + @DAY + ',' + @LATEST + ',' + @LATEST_FULL;
		SET @Create_View = '
		CREATE VIEW ' + @Table_name + ' AS 
		SELECT latest_full.* FROM ' + @LATEST_FULL + ' AS latest_full
		LEFT JOIN ' + @LATEST + ' AS latest ON latest.' + @IDName + ' = latest_full.' + @IDName + '	
		WHERE latest.' + @IDName + ' IS NULL
		';
		SET @autoLASR = 0;
	END

--------------------------------------
-- AGE: OLDEST
--
-- Requires:
-- HIST
--
--------------------------------------
-- Note: Requires HIST
END ELSE IF @Age LIKE '%OLDEST%' BEGIN
	SET @Dependencies_list = @HIST;
	-- Determine data source for _OLDEST
	DECLARE @Oldest_source NVARCHAR(50);
	SET @Oldest_source = @HIST;
	-- Build OLDEST
	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS
	SELECT ' +
	' temp.* FROM '  + @Oldest_source + ' AS temp
	INNER JOIN
	(
		SELECT ' + @IDName + ', 
		MIN(' + @DateTimeName + ') AS LastTime
		FROM
		' + @Oldest_source + '
		WHERE ' + @DataName + ' > 0 
		GROUP BY ' + @IDName + '
	) AS recent
	ON
	temp.' + @IDName + ' = recent.' + @IDName + '
	AND temp.' + @DateTimeName + ' = recent.LastTime
	';

END -- end OLDEST

--------------------------------------
-- CUSTOM Tables
--
-- Requires:
-- CREATE_CUSTOM.sh must have
-- been run at least once per table
--------------------------------------
IF EXISTS(SELECT * FROM CEVAC_TABLES WHERE TableName = @Table_name) AND @isCustom = 1 AND @Age = 'HIST' BEGIN
	SELECT 'Custom' AS 'Custom';
	SET @Dependencies_list = (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @Table_name);
	DECLARE @createTableName NVARCHAR(MAX);
	-- CREATE_[TableName] is a procedure automatically generated when CREATE_CUSTOM.sh is run
	SET @createTableName = 'CREATE_' + @Table_name;
	IF @execute = 1 EXEC @createTableName @Definition_OUT = @Create_View OUTPUT;
	SELECT @createTableName AS 'Create Custom Table';
END



--------------------------------------
-- Execute and create the view
--------------------------------------
PRINT @Create_View;
IF @execute = 1 AND @Create_View IS NOT NULL BEGIN
	PRINT('Create view:');
	PRINT(@Create_View);
	EXEC(@Create_View);
	DELETE FROM CEVAC_TABLES WHERE TableName = @Table_name;
	IF NOT EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @Table_name) BEGIN
		INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Definition, Dependencies, customLASR, autoCACHE, autoLASR)
			VALUES (
				@Building,
				@Metric,
				@Age,
				@Table_name,
				isnull(@DateTimeName,@RemoteUTCName),
				isnull(@IDName,@RemotePSIDName),
				isnull(@AliasName,'Alias'),
				isnull(@DataName, @RemoteActualValueName),
				isnull(@isCustom,0),
				@Create_View,
				@Dependencies_list,
				isnull(@customLASR,0),
				isnull(@autoCACHE,0),
				isnull(@autoLASR,0)
			)
	END
END


--------------------------------------
-- Create HIST API Table
--------------------------------------
IF @Age LIKE '%HIST%' BEGIN
	DECLARE @Drop_API NVARCHAR(MAX);
	SET @Drop_API = 'DROP VIEW ' + @HIST;
	IF OBJECT_ID(@HIST, 'V') IS NOT NULL BEGIN
		SELECT @Drop_API AS 'DROP _HIST API View'
		IF @execute = 1 BEGIN
			EXEC(@Drop_API);
			IF EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @HIST) BEGIN
				DELETE FROM CEVAC_TABLES WHERE TableName = @HIST;
			END
		END
	END

	DECLARE @_HIST_source NVARCHAR(MAX);
	DECLARE @Create_API_View NVARCHAR(MAX);
	-- _HIST selects from _VIEW if _CACHE does not exist
	IF OBJECT_ID(@HIST_CACHE, 'U') IS NOT NULL SET @_HIST_source = @HIST_CACHE;
	ELSE SET @_HIST_source = @HIST_VIEW;

	SET @DateTimeName = (SELECT TOP 1 DateTimeName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST');
	SET @AliasName = (SELECT TOP 1 AliasName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST');
	SET @IDName = (SELECT TOP 1 IDName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST');
	SET @DataName = ISNULL((SELECT TOP 1 DataName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'),@DataName);
	SET @isCustom = (SELECT TOP 1 isCustom FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST');
	SET @autoCACHE = 0;
	SET @autoLASR = 1;
--	SET @customLASR = (SELECT TOP 1 customLASR FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST');

	IF @DateTimeName IS NULL OR @AliasName IS NULL OR @DataName IS NULL OR @IDName IS NULL BEGIN
		SET @error = 'Make sure CEVAC_' + @Building + '_' + @Metric + '_HIST_VIEW is in CEVAC_TABLES';
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @Table_name;
		RAISERROR(@error, 11, 1);
		RETURN
	END


	SET @Create_API_View = '
	CREATE VIEW ' + @HIST + '
	AS 
	SELECT * FROM ' + @_HIST_source;
	SELECT @Create_API_View AS '_HIST_API';
	IF @execute = 1 BEGIN
		EXEC(@Create_API_View);
		IF NOT EXISTS (SELECT * FROM CEVAC_TABLES WHERE TableName = @HIST) BEGIN
			INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Definition, Dependencies, customLASR, autoCACHE, autoLASR)
			VALUES (
				@Building,
				@Metric,
				@Age,
				@HIST,
				@DateTimeName,
				@IDName,
				@AliasName,
				@DataName,
				isnull(@isCustom,0),
				@Create_View,
				@_HIST_source,
				isnull(@customLASR,0),
				isnull(@autoCACHE,0),
				isnull(@autoLASR,0)
			);
		END
	END
END

