
CREATE VIEW CEVAC_ASC_TEMP_15M AS

SELECT
	xref.Alias as Alias, val.UTCDateTime, val.ActualValue, DATEPART(year, UTCDateTime) AS Year, DATEPART(month, UTCDateTime) AS Month, DATEPART(day, UTCDateTime) AS Day
FROM
	[130.127.238.129].JCIHistorianDB.dbo.tblActualValueFloat as val
	INNER JOIN  
	[130.127.238.129].JCIHistorianDB.dbo.tblPointSlice as ps ON ps.PointSliceID = val.PointSliceID
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblPoint as pt ON ps.PointID = pt.PointID
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID
	INNER JOIN
	dbo.WATT_TEMP_XREF as xref ON xref.PointSliceID = val.PointSliceID

WHERE val.PointSliceID IN
(
	SELECT DISTINCT
		ps.PointSliceID
	FROM
		[130.127.238.129].JCIHistorianDB.dbo.tblPoint AS pt
		INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblPointSlice AS ps ON pt.PointID = ps.PointID
	WHERE
(UnitOfMeasureID  = '64')
AND (  PointName LIKE '%ADX:ACAD%')
AND (
	PointName LIKE '%HTG%SP%'
	OR PointName LIKE '%CLG%SP%'	
	OR PointName LIKE '%ZN%T%'
	OR PointName LIKE '%SLAB%'
	OR PointName LIKE '%CRAC%'
) AND UTCDateTime <= GETDATE() AND UTCDateTime >= DATEADD(minute, -60, GETDATE())


)
