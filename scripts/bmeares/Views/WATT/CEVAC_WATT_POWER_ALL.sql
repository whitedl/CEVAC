
CREATE VIEW CEVAC_WATT_POWER_ALL AS

SELECT
	ps.PointSliceID as PointSliceID, val.UTCDateTime, val.ActualValue, DATEPART(year, UTCDateTime) AS Year, DATEPART(month, UTCDateTime) AS Month, DATEPART(day, UTCDateTime) AS Day
FROM
	[130.127.238.129].JCIHistorianDB.dbo.tblActualValueFloat as val
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblPointSlice as ps ON ps.PointSliceID = val.PointSliceID
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblPoint as pt ON ps.PointID = pt.PointID
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID

WHERE val.PointSliceID IN
(
	SELECT DISTINCT
		ps.PointSliceID
	FROM
		[130.127.238.129].JCIHistorianDB.dbo.tblPoint AS pt
		INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblPointSlice AS ps ON pt.PointID = ps.PointID
	WHERE
(UnitOfMeasureID  = '48')
AND (  PointName LIKE '%WATT%')
)
