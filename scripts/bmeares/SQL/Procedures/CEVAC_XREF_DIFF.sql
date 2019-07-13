--IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_XREF_DIFF') DROP PROCEDURE CEVAC_XREF_DIFF;
--GO
--SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
--GO
--CREATE PROCEDURE CEVAC_XREF_DIFF
--	@Building NVARCHAR(30),
--	@Metric NVARCHAR(30),
--	@keys_list NVARCHAR(500),
--	@unitOfMeasureID int
--AS

--DECLARE @keys_list_query NVARCHAR(500);
--SET @keys_list_query = ' INNER JOIN ListTable(''' + @keys_list + ''') AS Params ON pt.PointName LIKE ''%'' + Params.items + ''%''';

DECLARE @keys_list NVARCHAR(500);
SET @keys_list = '';

WITH PSIDs AS (
	SELECT ps.PointSliceID, pt.PointName, units.UnitOfMeasureID
	FROM
		[130.127.238.129].JCIHistorianDB.dbo.tblPointSlice as ps
		INNER JOIN
		[130.127.238.129].JCIHistorianDB.dbo.tblPoint as pt ON ps.PointID = pt.PointID
		INNER JOIN
		[130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID
		INNER JOIN ListTable(@keys_list) AS Params ON pt.PointName LIKE '%' + Params.items + '%'

		WHERE pt.PointName LIKE '%ADX:WATT%'
		AND units.UnitOfMeasureID = 64
		AND pt.PointName NOT LIKE '%CHW%'
		AND pt.PointName NOT LIKE '%EFF%'
		AND pt.PointName NOT LIKE '%-SP%'
), composite AS (
	SELECT xref.Alias, xref.PointSliceID AS 'XREF_PointSliceID', PSIDs.PointSliceID AS 'JCI_PointSliceID', xref.ObjectName AS 'XREF_PointName', PSIDs.PointName AS 'JCI_PointName', PSIDs.UnitOfMeasureID
	FROM PSIDs
	LEFT JOIN CEVAC_WATT_TEMP_XREF AS xref ON PSIDs.PointSliceID = xref.PointSliceID
) SELECT * FROM composite
WHERE Alias IS NULL


