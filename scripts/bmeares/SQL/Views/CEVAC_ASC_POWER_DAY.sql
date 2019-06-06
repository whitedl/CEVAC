IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_ASC_POWER_DAY'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_ASC_POWER_DAY
END
GO
CREATE VIEW CEVAC_ASC_POWER_DAY AS

SELECT
	val.PointSliceID, val.UTCDateTime, val.ActualValue, DATEPART(year, UTCDateTime) AS Year, DATEPART(month, UTCDateTime) AS Month, DATEPART(day, UTCDateTime) AS Day
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
(UnitOfMeasureID  = '48')
AND (  PointName LIKE '%ADX:ACAD%')
AND UTCDateTime <= GETDATE() AND UTCDateTime >= DATEADD(day, -1, GETDATE())


)
