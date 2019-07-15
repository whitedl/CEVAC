IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_VIEW') DROP PROCEDURE CEVAC_VIEW;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_VIEW
	@Building NVARCHAR(30),
	@Metric NVARCHAR(30),
	@Age NVARCHAR(30),
	@keys_list NVARCHAR(500) = '',
	@unitOfMeasureID int = NULL
AS

DECLARE @building_key nvarchar(100);
DECLARE @execute INT;
SET @execute = 1;

SET @building_key = (SELECT RTRIM(BuildingKey) FROM CEVAC_BUILDING_INFO WHERE BuildingSName = @Building);
--IF @building_key IS NULL BEGIN
--	RAISERROR('Add BuildingSName to CECAC_BUILDING_INFO', 0, 1);
--	RETURN
--END

DECLARE @Table_name nvarchar(100);
DECLARE @HIST_VIEW NVARCHAR(200);
DECLARE @HIST_CACHE NVARCHAR(200);
DECLARE @HIST NVARCHAR(200);
DECLARE @DAY NVARCHAR(200);
DECLARE @LATEST NVARCHAR(200);
DECLARE @LATEST_FULL NVARCHAR(200);
DECLARE @LATEST_BROKEN NVARCHAR(200);
DECLARE @OLDEST NVARCHAR(200);
DECLARE @XREF nvarchar(200);
DECLARE @PXREF nvarchar(200);
-- Drop temp table if exists
IF OBJECT_ID('tempdb.dbo.#cevac_vars', 'U') IS NOT NULL DROP TABLE #cevac_vars;
IF OBJECT_ID('tempdb.dbo.#cevac_metric_params', 'U') IS NOT NULL DROP TABLE #cevac_metric_params;


-- Create temporary table for variables
CREATE TABLE #cevac_vars(
	Metric nvarchar(30),
	Building nvarchar(30),
	Age nvarchar(30),
	Table_name nvarchar(100),
	XREF nvarchar(100),
	building_key nvarchar(100),
	keys_list nvarchar(500),
	unitOfMeasureID int
)
CREATE TABLE #cevac_metric_params(Params nvarchar(100))

-- Generate table names
-- Reference names
SET @HIST_VIEW = 'CEVAC_' + @Building + '_' + @Metric + '_HIST_VIEW';
SET @HIST_CACHE = 'CEVAC_' + @Building + '_' + @Metric + '_HIST_CACHE';
SET @HIST = 'CEVAC_' + @Building + '_' + @Metric + '_HIST';
SET @DAY = 'CEVAC_' + @Building + '_' + @Metric + '_DAY';
SET @LATEST = 'CEVAC_' + @Building + '_' + @Metric + '_LATEST';
SET @LATEST_FULL = 'CEVAC_' + @Building + '_' + @Metric + '_LATEST_FULL';
SET @LATEST_BROKEN = 'CEVAC_' + @Building + '_' + @Metric + '_LATEST_BROKEN';
SET @OLDEST = 'CEVAC_' + @Building + '_' + @Metric + '_OLDEST';

-- Current name
IF @Age LIKE '%HIST%' SET @Table_name = CONCAT('CEVAC_', @Building, '_', @Metric, '_', @Age, '_VIEW')
ELSE SET @Table_name = CONCAT('CEVAC_', @Building, '_', @Metric, '_', @Age);
SELECT @Table_name AS 'Table_name init';
SET @XREF = CONCAT('CEVAC_', @Building, '_', @Metric, '_XREF');
IF @Metric = 'POWER_SUMS' SET @XREF = CONCAT('CEVAC_', @Building, '_POWER_XREF');
SET @PXREF = CONCAT('CEVAC_', @Building, '_', @Metric, '_PXREF');
IF @Metric = 'POWER_RAW' SET @XREF = CONCAT('CEVAC_', @Building, '_', REPLACE(@Metric, 'POWER_RAW', 'POWER'), '_XREF');
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF) SET @XREF = NULL;

-- add quotes for regex search
SET @building_key = '''' + @building_key + '''';

-- add variables to temp table
INSERT INTO #cevac_vars SELECT @Metric, @Building, @Age, @Table_name, @XREF, @building_key,
--@metric_key,
@keys_list, @unitOfMeasureID

--------------------------------
-- Verify everything is in order
--------------------------------
IF @Age LIKE 'HIST' BEGIN
	IF OBJECT_ID(@XREF) IS NULL AND OBJECT_ID(@PXREF) IS NULL AND @building_key IS NOT NULL BEGIN
		RAISERROR('HIST requires XREF or PXREF', 11, 1);
		RETURN
	END
END
IF @Age LIKE 'DAY' BEGIN
	IF OBJECT_ID(@HIST) IS NULL BEGIN
		RAISERROR('DAY requires HIST', 11, 1);
		RETURN
	END
END
IF @Age LIKE 'LATEST%' BEGIN
	IF OBJECT_ID(@DAY) IS NULL OR OBJECT_ID(@HIST) IS NULL BEGIN
		RAISERROR('LATEST requires HIST and DAY', 11, 1);
		RETURN
	END
END
IF @Age LIKE 'OLDEST%' BEGIN
	IF OBJECT_ID(@HIST) IS NULL BEGIN
		RAISERROR('OLDEST requires HIST', 11, 1);
		RETURN
	END
END
IF @Age LIKE 'LATEST_BROKEN' BEGIN
	IF OBJECT_ID(@DAY) IS NULL OR OBJECT_ID(@HIST) IS NULL OR OBJECT_ID(@LATEST) IS NULL OR OBJECT_ID(@LATEST_FULL) IS NULL BEGIN
		RAISERROR('LATEST_BROKEN requires HIST, DAY, LATEST_FULL, and LATEST', 11, 1);
		RETURN
	END
END
DECLARE @Dependencies_list NVARCHAR(MAX);
SET @Dependencies_list = '';
-- Verify all dependencies (runs only if table is in CEVAC_TABLES)
IF EXISTS (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @Table_name) BEGIN
	
	DECLARE @Dependencies_query NVARCHAR(MAX);
	SET @Dependencies_query = '';
	DECLARE @dependency NVARCHAR(200);
	DECLARE @dependency_query NVARCHAR(500);
	SET @Dependencies_list = (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @Table_name);
	SELECT * INTO #cevac_dep FROM ListTable(@Dependencies_list);
	DECLARE @i INT;
	SET @i = 100;
	WHILE (EXISTS(SELECT 1 FROM #cevac_dep) AND @i > 0) BEGIN
		SET @dependency = (SELECT TOP 1 * FROM #cevac_dep);
		DELETE TOP(1) FROM #cevac_dep;
		SET @dependency_query = '
		IF OBJECT_ID(''' + @dependency + ''') IS NULL BEGIN
			RAISERROR(''' + @Table_name + ' requires ' + @dependency + ''', 11, 1);
			RETURN
		END
		';

		SET @Dependencies_query = @Dependencies_query + @dependency_query;

		SET @i = @i - 1;
	END
	IF @execute = 1 EXEC(@Dependencies_query);
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
DECLARE @unitOfMeasureID_query NVARCHAR(50);
SET @unitOfMeasureID_query = (SELECT CASE WHEN @unitOfMeasureID IS NOT NULL THEN ' AND units.UnitOfMeasureID = ''' + CAST(@unitOfMeasureID AS NVARCHAR(30)) + '''' ELSE NULL END)
DECLARE @Age_query NVARCHAR(200);
IF @Age = 'DAY' SET @Age_query = ' AND UTCDateTime <= GETUTCDATE() AND UTCDateTime >= DATEADD(day, -1, GETUTCDATE())';
DECLARE @XREF_query NVARCHAR(200);
SET @XREF_query = 'INNER JOIN ' + @XREF + ' AS xref on xref.PointSliceID = ps.PointSliceID';
DECLARE @Alias_query NVARCHAR(200);
SET @Alias_query = ' xref.Alias AS Alias, ';
DECLARE @Alias_or_PSID NVARCHAR(20);
SET @Alias_or_PSID = 'Alias';
DECLARE @DateTimeName NVARCHAR(50);
DECLARE @AliasName NVARCHAR(50);
DECLARE @isCustom BIT;

-- If XREF doesn't exist, select PointSliceID instead
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF)
BEGIN
	SET @XREF_query = NULL;
	SET @Alias_or_PSID = 'PointSliceID';
	SET @Alias_query = 'ps.PointSliceID AS PointSliceID, ';
END ELSE BEGIN -- XREF exists
	-- Insert XREF into CEVAC_TABLES
	SELECT 'Adding XREF to table: ' + @XREF AS 'XREF';
	IF @execute = 1 BEGIN
		DELETE FROM CEVAC_TABLES WHERE TableName = @XREF;
		INSERT INTO CEVAC_TABLES(BuildingSName, Metric, Age, TableName, DateTimeName, AliasName)
		VALUES (@Building, @Metric, 'XREF', @XREF, 'PointSliceID', 'Alias');
	END
END



-------------------------------------------------------
-- There exists a similar table within CEVAC_TABLES
-- Grab AliasName, DateTimeName, and isCustom from HIST
-------------------------------------------------------
IF @Age != 'XREF' AND EXISTS (SELECT TOP 1 TableName FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age != 'XREF') BEGIN
	SET @DateTimeName = ISNULL((SELECT TOP 1 RTRIM(DateTimeName) FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'),'UTCDateTime'); -- DEFAULT
	SET @AliasName = ISNULL((SELECT TOP 1 RTRIM(AliasName) FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'),@Alias_or_PSID);   -- DEFAULT
	SET @isCustom = ISNULL((SELECT TOP 1 isCustom FROM CEVAC_TABLES WHERE BuildingSName = @Building AND Metric = @Metric AND Age = 'HIST'),0);-- DEFAULT
END



SELECT @DateTimeName AS 'DateTimeName';
SELECT @AliasName AS 'AliasName';
SELECT @isCustom AS 'isCustom'

-- build view query
DECLARE @Create_View nvarchar(MAX);


-----------------------------------------------
-- Age: PXREF (standard)
--
-- Requires:
-- None (init standard bootstrap with PXREF)
-----------------------------------------------
IF @Age LIKE '%PXREF%' BEGIN
	DECLARE @tblUnitOfMeasure_join NVARCHAR(500);
	IF @unitOfMeasureID_query IS NOT NULL BEGIN
		SET @tblUnitOfMeasure_join = '
		INNER JOIN
		[130.127.238.129].JCIHistorianDB.dbo.tblPointSlice as ps ON ps.PointSliceID = val.PointSliceID
		INNER JOIN
		[130.127.238.129].JCIHistorianDB.dbo.tblPoint as pt ON ps.PointID = pt.PointID
		INNER JOIN
		[130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID
		';
	END

	DECLARE @PXREF_drop NVARCHAR(MAX);
	SET @PXREF_drop = '
		IF OBJECT_ID(''dbo.' + @PXREF + ''', ''U'') IS NOT NULL DROP TABLE ' + @PXREF + ';';

	-- Drop PXREF if it exists
	SELECT @PXREF_drop AS 'Drop PXREF';
	IF @execute = 1 BEGIN
		EXEC(@PXREF_drop);
		IF EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @PXREF) BEGIN
			DELETE FROM CEVAC_TABLES WHERE TableName = @PXREF;
		END

	END

	-- Create PXREF
	DECLARE @PXREF_query NVARCHAR(MAX);
	SET @PXREF_query = '
		SELECT DISTINCT
			ps.PointSliceID, pt.PointName, units.UnitOfMeasureID
		INTO ' + isnull(@PXREF, 'PXREF ERROR') + '
		FROM
			[130.127.238.129].JCIHistorianDB.dbo.tblPoint AS pt
			INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblPointSlice AS ps ON pt.PointID = ps.PointID 
			INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID
			' + isnull(@keys_list_query, 'Keys List ERROR') + '
		WHERE
		( PointName LIKE ' + isnull(@building_key, 'Building Key ERROR') + ')
		' + isnull(@unitOfMeasureID_query, '') + '
	';
	SELECT @PXREF_query AS 'Create PXREF';
	IF @execute = 1 BEGIN 
		EXEC(@PXREF_query);
		IF NOT EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @PXREF) BEGIN
		INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, Definition, Dependencies)
		VALUES (
			@Building,
			@Metric,
			@Age,
			@PXREF,
			'UTCDateTime',
			@Alias_or_PSID,
			@PXREF_query,
			NULL
		)
		END
	END
	RETURN
END


------------------------------------------------------------
-- Age: HIST_VIEW (standard)
--
-- Requires:
-- XREF or PXREF (only if standard)
-- Note: Dependencies left NULL for non-standard HIST tables
------------------------------------------------------------
ELSE IF @Age LIKE '%HIST%' AND @isCustom != 1 BEGIN
	SELECT 'HIST';
	DECLARE @PSID_source NVARCHAR(500);
	IF @Alias_or_PSID = 'Alias' SET @PSID_source = '
	SELECT PointSliceID FROM ' + @XREF + '
	';
	ELSE SET @PSID_source = '
		SELECT PointSliceID FROM ' + @PXREF + ' ';


SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS

	WITH original AS (
		SELECT
		' + @Alias_query + '
		val.UTCDateTime, dbo.ConvertUTCToLocal(val.UTCDateTime) AS ETDateTime, val.ActualValue 
		FROM
			[130.127.238.129].JCIHistorianDB.dbo.tblActualValueFloat as val
			INNER JOIN
			[130.127.238.129].JCIHistorianDB.dbo.tblPointSlice as ps ON ps.PointSliceID = val.PointSliceID
			INNER JOIN
			[130.127.238.129].JCIHistorianDB.dbo.tblPoint as pt ON ps.PointID = pt.PointID
			INNER JOIN
			[130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID
			' + isnull(@XREF_query, '') + '

		WHERE val.PointSliceID IN
		(' + @PSID_source + '
		)' + isnull(@unitOfMeasureID_query, '') + ' ';


	-- End of original
	SET @Create_View = @Create_View + '
	) SELECT * FROM original
	';

	SET @isCustom = 0;
	SET @Dependencies_list = NULL;

END -- END of _HIST_VIEW
		
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
	

-----------------------------------------------
-- Ages: LATEST, LATEST_FULL, and LATEST_BROKEN
--
-- Requires:
-- HIST, DAY
-- LATEST, LATEST_FULL (for LATEST_BROKEN)
-----------------------------------------------
END ELSE IF @Age LIKE '%LATEST%' BEGIN
	SET @Dependencies_list = @HIST + ',' + @DAY;
	-- Determine data source for _LATEST
	DECLARE @Latest_source NVARCHAR(500);
	IF @Age LIKE '%FULL%' SET @Latest_source = @HIST;
	ELSE SET @Latest_source = @DAY;
	-- Build LATEST
	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS
	SELECT ' +
--	' temp.' + @Alias_or_PSID + ', ' +
	' temp.* FROM '  + @Latest_source + ' AS temp
	INNER JOIN
	(
		SELECT ' + @AliasName + ', 
		MAX(' + @DateTimeName + ') AS LastTime
		FROM
		' + @Latest_source + '
		GROUP BY ' + @AliasName + '
	) AS recent
	ON
	temp.' + @AliasName + ' = recent.' + @AliasName + '
	AND temp.' + @DateTimeName + ' = recent.LastTime
	';

	-- NOTE: LATEST and LATEST_FULL must exist
	IF @Age LIKE '%BROKEN%' BEGIN
		SET @Dependencies_list = @HIST + ',' + @DAY + ',' + @LATEST + ',' + @LATEST_FULL;
		SET @Create_View = '
		CREATE VIEW ' + @Table_name + ' AS 
		SELECT latest_full.* FROM ' + @LATEST_FULL + ' AS latest_full
		LEFT JOIN ' + @LATEST + ' AS latest ON latest.' + @AliasName + ' = latest_full.' + @AliasName + '	
		WHERE latest.' + @AliasName + ' IS NULL
		';
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
--	' temp.' + @Alias_or_PSID + ', ' +
	' temp.* FROM '  + @Oldest_source + ' AS temp
	INNER JOIN
	(
		SELECT ' + @AliasName + ', 
		MIN(' + @DateTimeName + ') AS LastTime
		FROM
		' + @Oldest_source + '
		GROUP BY ' + @AliasName + '
	) AS recent
	ON
	temp.' + @AliasName + ' = recent.' + @AliasName + '
	AND temp.' + @DateTimeName + ' = recent.LastTime
	';

END -- end OLDEST

--------------------------------------
-- CUSTOM Tables
--
-- Requires:
-- CREATE_CUSTOM.sh must have
-- been run at least once
--------------------------------------
IF @isCustom = 1 AND @Age = 'HIST' BEGIN
	SELECT 'Custom' AS 'Custom';
	SET @Dependencies_list = (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @Table_name);
	DECLARE @createTableName NVARCHAR(MAX);
	SET @createTableName = 'CREATE_' + @Table_name;
	IF @execute = 1 EXEC @createTableName @Definition_OUT = @Create_View OUTPUT;
	SELECT @createTableName AS 'Create Custom Table';
END




--------------------------------------
-- Execute and create the view
--------------------------------------
SELECT @Create_View AS 'Create View'
IF @execute = 1 AND @Create_View IS NOT NULL BEGIN
	EXEC(@Create_View)

	IF NOT EXISTS (SELECT TableName FROM CEVAC_TABLES WHERE TableName = @Table_name) BEGIN
		INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, isCustom, Definition, Dependencies)
			VALUES (
				@Building,
				@Metric,
				@Age,
				@Table_name,
				isnull(@DateTimeName,'UTCDateTime'),
				isnull(@AliasName,'Alias'),
				@isCustom,
				@Create_View,
				@Dependencies_list
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

	--DECLARE @DROP_HIST NVARCHAR(50);
	--SET @DROP_HIST = 'DROP VIEW ' + REPLACE(@Table_name, '_VIEW', '');
	--IF OBJECT_ID(REPLACE(@Table_name, '_VIEW', ''), 'V') IS NOT NULL EXEC @DROP_HIST;

	SET @Create_API_View = '
	CREATE VIEW ' + @HIST + '
	AS 
	SELECT * FROM ' + @_HIST_source;
	SELECT @Create_API_View AS '_HIST_API';
	IF @execute = 1 BEGIN
		EXEC(@Create_API_View);
		IF NOT EXISTS (SELECT * FROM CEVAC_TABLES WHERE TableName = @HIST) BEGIN
			INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, Definition, Dependencies)
			VALUES (
				@Building,
				@Metric,
				@Age,
				@HIST,
				@DateTimeName,
				@AliasName,
				@Create_API_View,
				@_HIST_source
			)
		END
	END
END


-- Cleanup
DROP TABLE #cevac_vars

DROP TABLE #cevac_metric_params
