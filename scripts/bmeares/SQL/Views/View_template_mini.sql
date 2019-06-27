DECLARE @Building nvarchar(30);
DECLARE @Metric nvarchar(30);
DECLARE @Age nvarchar(30);
DECLARE @building_key nvarchar(30);
DECLARE @unitOfMeasureID int;
DECLARE @keys_list nvarchar(500);
SET @Building = '#BUILDING#';
SET @Metric = '#METRIC#';
SET @Age = '#AGE#';
SET @keys_list = '#KEYS_LIST#';
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
IF OBJECT_ID('tempdb.dbo.#cevac_vars', 'U') IS NOT NULL DROP TABLE #cevac_vars;
IF OBJECT_ID('tempdb.dbo.#cevac_metric_params', 'U') IS NOT NULL DROP TABLE #cevac_metric_params;

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
SET @Table_name = CONCAT('CEVAC_', @Building, '_', @Metric, '_', @Age);
SET @XREF = CONCAT('CEVAC_', @Building, '_', @Metric, '_XREF');
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF) SET @XREF = NULL;
SET @building_key = CONCAT('''', @building_key, '''');
INSERT INTO #cevac_vars SELECT @Metric, @Building, @Age, @Table_name, @XREF, @building_key, @keys_list, @unitOfMeasureID
IF EXISTS(
	SELECT * FROM INFORMATION_SCHEMA.TABLES
	WHERE TABLE_SCHEMA = 'dbo'
	AND TABLE_NAME=@Table_name
	AND TABLE_TYPE ='VIEW'
) BEGIN
	DECLARE @ExecSQL NVARCHAR(300);
	SET @ExecSQL = CONCAT('DROP VIEW ', @Table_name);
	EXEC(@ExecSQL);
END

DECLARE @keys_list_query NVARCHAR(500);
SET @keys_list_query = 'INNER JOIN ListTable(''' + @keys_list + ''') AS Params ON pt.PointName LIKE ''%'' + Params.items + ''%''';
DECLARE @unitOfMeasureID_query NVARCHAR(50);
SET @unitOfMeasureID_query = (SELECT CASE WHEN @unitOfMeasureID IS NOT NULL THEN ' AND UnitOfMeasureID = ''' + CAST(@unitOfMeasureID AS NVARCHAR(30)) + '''' ELSE NULL END)
DECLARE @Age_query NVARCHAR(200);
IF @Age = 'DAY' SET @Age_query = 'AND UTCDateTime <= GETUTCDATE() AND UTCDateTime >= DATEADD(day, -1, GETUTCDATE())';
DECLARE @XREF_query NVARCHAR(200);
SET @XREF_query = 'INNER JOIN ' + @XREF + 'AS xref on xref.PointSliceID = ps.PointSliceID';
DECLARE @Alias_query NVARCHAR(200);
SET @Alias_query = 'xref.Alias AS Alias, ';
DECLARE @Alias_or_PSID NVARCHAR(20);
SET @Alias_or_PSID = 'Alias';

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = @XREF)
	BEGIN
		SET @XREF_query = NULL;
		SET @Alias_or_PSID = 'PointSliceID';
		SET @Alias_query = 'ps.PointSliceID AS PointSliceID, ';
	END

DECLARE @Create_View nvarchar(4000);
IF @Age NOT LIKE '%LATEST%' BEGIN
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
	DECLARE @Latest_source NVARCHAR(30);
	IF @Age LIKE '%FULL%' SET @Latest_source = 'CEVAC_' + @Building + '_' + @Metric + '_HIST';
	ELSE SET @Latest_source = 'CEVAC_' + @Building + '_' + @Metric + '_DAY';
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
EXEC(@Create_View)
DROP TABLE #cevac_vars
DROP TABLE #cevac_metric_params
