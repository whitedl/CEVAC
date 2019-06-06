IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_VIEW') DROP PROCEDURE CEVAC_VIEW;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_VIEW
	@Building NVARCHAR(30),
	@Metric NVARCHAR(30),
	@Age NVARCHAR(30),
	@keys_list NVARCHAR(500),
	@unitOfMeasureID int
AS


DECLARE @building_key nvarchar(30);


-- #####################################################################################################
-- Configure Table information here. See instructions below for more information
--SET @Building = '#BUILDING#';
--SET @Metric = '#METRIC#';
--SET @Age = '#AGE#';
--SET @keys_list = '#KEYS_LIST#';   -- Comma-separated PointName substrings for JCIHistorianDB

-- Optional: comment these out to omit from search
--SET @unitOfMeasureID = '48';

-- #####################################################################################################

-- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
-- INSTRUCTIONS
-- Edit the variables above to create a new view. Below are descriptions of each variable.
-- 
-- Building:
--   Use the standard CEVAC building names (WATT, ASC, COOPER, FLUOR, etc. Full list below).
--
-- Metric:
--   Describes the content of the table (WATER, POWER, TEMP, IAQ, etc).
--
-- Age:
--   ____CEVAC Name____________________Description___________________________________
--   HIST           |  All data from beginning of time
--   DAY            |  All data from last 24 hours (rolling)
--   LATEST         |  Most recent entry from each PointSliceID (searches DAY)
--   LATEST_FULL    |  Most recent entry from each PointSliceID (searches HIST)
--
-- keys_list:
--   Comma-separated list of PointName substrings.
--   e.g. CO2,-Q,ZN-T,SLAB,etc
--
-- unitOfMeasureID (optional):
--   Additional qualifier to restrict PointSliceIDs by measurement type.
--   Below are some common unitsOfMeasureIDs. Visit http://130.127.218.148/requests/units.php
--   for the complete list.
--   ____Name_________________UnitOfMeasureID____
--   degrees-Fahrenheit    |  64
--   kilowatts             |  48
--   kilowatt-hours        |  19
--   parts-per-million     |  96
--   us-gallons            |  83
-- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::




-- Selects builing_key from Building
--   building_key: Keyword for extracting Pointnames from JCIHistorianDB by building.
--   ____CEVAC Name____________________Keyword_______________________________________
--   ASC            |  ADX:ACAD
--   COOPER         |  ADX:CL-
--   FIKE           |  ADX:FIKE
--   FLUOR          |  ADX:FD and ADX:FLUOR (therefore ADX:F[DL])
--   HOLMES         |  ADX:HH and HOLMES
--   LEE_III        |  ADX:LEE??? (groups all Lees together)
--   LITTLE_JOHN    |  ADX:LJ
--   MCCABE         |  ADX:MH
--   RIGGS          |  ADX:RIGGS (ADX:RH-? Not included but worth investigating)
--   WATT           |  ADX:WATT
IF @Building = 'ASC' SET @building_key = '%ADX:ACAD%'
ELSE IF @Building = 'COOPER' SET @building_key = '%ADX:CL-%'
ELSE IF @Building = 'FIKE' SET @building_key = '%ADX:FIKE%'
ELSE IF @Building = 'FLUOR' SET @building_key = '%ADX:F[DL]%'
ELSE IF @Building = 'HOLMES' SET @building_key = '%ADX:HH%'
ELSE IF @Building = 'LEE_III' SET @building_key = '%ADX:LEE%'
ELSE IF @Building = 'LITTLE_JOHN' SET @building_key = '%ADX:LJ%'
ELSE IF @Building = 'MCCABE' SET @building_key = '%ADX:MH%'
ELSE IF @Building = 'RIGGS' SET @building_key = '%ADX:RIGGS%'
ELSE IF @Building = 'WATT' SET @building_key = '%ADX:WATT%'


DECLARE @Table_name nvarchar(100);
DECLARE @XREF nvarchar(100);
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
	building_key nvarchar(30),
	keys_list nvarchar(500),
	unitOfMeasureID int
)
CREATE TABLE #cevac_metric_params(Params nvarchar(100))

-- Generate table names
SET @Table_name = CONCAT('CEVAC_', @Building, '_', @Metric, '_', @Age);
SET @XREF = CONCAT('CEVAC_', @Building, '_', @Metric, '_XREF');
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF) SET @XREF = NULL;

-- add quotes for regex search
SET @building_key = CONCAT('''', @building_key, '''');

-- add variables to temp table
INSERT INTO #cevac_vars SELECT @Metric, @Building, @Age, @Table_name, @XREF, @building_key,
--@metric_key,
@keys_list, @unitOfMeasureID


-- Drop and recreate view
--DECLARE @Table_name nvarchar(30);
--SET @Table_name = (SELECT Table_name FROM #cevac_vars);
IF EXISTS(
	SELECT * FROM INFORMATION_SCHEMA.TABLES
	WHERE TABLE_SCHEMA = 'dbo'
	AND TABLE_NAME=@Table_name
	AND TABLE_TYPE ='VIEW'
) BEGIN
	-- Drop view if it exists
	DECLARE @ExecSQL NVARCHAR(300);
	SET @ExecSQL = CONCAT('DROP VIEW ', @Table_name);
	EXEC(@ExecSQL);

END


-- rebuild variables from temp table
--DECLARE @Table_name nvarchar(100);
--SET @Table_name = (SELECT Table_name FROM #cevac_vars);
--DECLARE @Metric nvarchar(30);
--SET @Metric = (SELECT Metric FROM #cevac_vars);
--DECLARE @Building nvarchar(30);
--SET @Building = (SELECT Building FROM #cevac_vars);
--DECLARE @XREF nvarchar(30);
--SET @XREF = (SELECT XREF FROM #cevac_vars);
--DECLARE @building_key nvarchar(30);
--SET @building_key = (SELECT building_key FROM #cevac_vars);
--DECLARE @Age NVARCHAR(30);
--SET @Age = (SELECT Age FROM #cevac_vars);
--DECLARE @keys_list nvarchar(300);
--SET @keys_list = (SELECT keys_list FROM #cevac_vars);
--DECLARE @unitOfMeasureID INT;
--SET @unitOfMeasureID = (SELECT unitOfMeasureID FROM #cevac_vars);

-- Build subqueries from variables
DECLARE @keys_list_query NVARCHAR(500);
SET @keys_list_query = ' INNER JOIN ListTable(''' + @keys_list + ''') AS Params ON pt.PointName LIKE ''%'' + Params.items + ''%''';
DECLARE @unitOfMeasureID_query NVARCHAR(50);
SET @unitOfMeasureID_query = (SELECT CASE WHEN @unitOfMeasureID IS NOT NULL THEN ' AND UnitOfMeasureID = ''' + CAST(@unitOfMeasureID AS NVARCHAR(30)) + '''' ELSE NULL END)
DECLARE @Age_query NVARCHAR(200);
IF @Age = 'DAY' SET @Age_query = ' AND UTCDateTime <= GETUTCDATE() AND UTCDateTime >= DATEADD(day, -1, GETUTCDATE())';
DECLARE @XREF_query NVARCHAR(200);
SET @XREF_query = 'INNER JOIN ' + @XREF + ' AS xref on xref.PointSliceID = ps.PointSliceID';
DECLARE @Alias_query NVARCHAR(200);
SET @Alias_query = ' xref.Alias AS Alias, ';
DECLARE @Alias_or_PSID NVARCHAR(20);
SET @Alias_or_PSID = 'Alias';

-- If XREF doesn't exist, select PointSliceID instead
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF)
	BEGIN
		SET @XREF_query = NULL;
		SET @Alias_or_PSID = 'PointSliceID';
		SET @Alias_query = 'ps.PointSliceID AS PointSliceID, ';
	END

-- build view query
DECLARE @Create_View nvarchar(4000);
IF @Age NOT LIKE '%LATEST%' BEGIN
	-- Building HIST or DAY
	SET @Create_View = '
		CREATE VIEW ' + @Table_name + ' AS
		SELECT
		' + @Alias_query + '
		val.UTCDateTime, val.ActualValue, DATEPART(year, UTCDateTime) AS Year, DATEPART(month, UTCDateTime) AS Month, DATEPART(day, UTCDateTime) AS Day
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
		(
			SELECT DISTINCT
				ps.PointSliceID
			FROM
				[130.127.238.129].JCIHistorianDB.dbo.tblPoint AS pt
				INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblPointSlice AS ps ON pt.PointID = ps.PointID 
				' + @keys_list_query + '
			WHERE
		 ( PointName LIKE ' + @building_key + ')
	 		 ' + isnull(@unitOfMeasureID_query, '') + '
		)' + isnull(@Age_query, '');
END ELSE BEGIN
	-- Determine data source for _LATEST
	DECLARE @Latest_source NVARCHAR(30);
	IF @Age LIKE '%FULL%' SET @Latest_source = 'CEVAC_' + @Building + '_' + @Metric + '_HIST';
	ELSE SET @Latest_source = 'CEVAC_' + @Building + '_' + @Metric + '_DAY';
	-- Build LATEST
	SET @Create_View = '
	CREATE VIEW ' + @Table_name + ' AS
	SELECT
	temp.' + @Alias_or_PSID + ',
	temp.UTCDateTime, temp.ActualValue, temp.Year, temp.Month, temp.Day FROM '  + @Latest_source + ' AS temp
	INNER JOIN
	(
		SELECT ' + @Alias_or_PSID + ', 
		MAX(UTCDateTime) AS LastTime
		FROM
		' + @Latest_source + '
		GROUP BY ' + @Alias_or_PSID + '
	) AS recent
	ON
	temp.' + @Alias_or_PSID + ' = recent.' + @Alias_or_PSID + '
	AND temp.UTCDateTime = recent.LastTime
	';
END

-- Execute to create the view
EXEC(@Create_View)


-- Cleanup
DROP TABLE #cevac_vars

DROP TABLE #cevac_metric_params
