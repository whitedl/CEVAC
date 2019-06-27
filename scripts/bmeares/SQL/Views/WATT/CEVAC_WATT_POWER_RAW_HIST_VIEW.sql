IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_POWER_RAW_HIST_VIEW'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_WATT_POWER_RAW_HIST_VIEW
END
GO
CREATE VIEW CEVAC_WATT_POWER_RAW_HIST_VIEW AS

SELECT
--	ps.PointSliceID as PointSliceID,
	xref.Alias as Alias,
	val.UTCDateTime, val.ActualValue
FROM
	[130.127.238.129].JCIHistorianDB.dbo.tblActualValueFloat as val
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblPointSlice as ps ON ps.PointSliceID = val.PointSliceID
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblPoint as pt ON ps.PointID = pt.PointID
	INNER JOIN
	[130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure as units ON units.UnitOfMeasureID = pt.UnitOfMeasureID
	INNER JOIN
	dbo.CEVAC_WATT_POWER_XREF as xref on xref.PointSliceID = ps.PointSliceID

WHERE val.PointSliceID IN
(
	SELECT DISTINCT
		ps.PointSliceID
	FROM
		[130.127.238.129].JCIHistorianDB.dbo.tblPoint AS pt
		INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblPointSlice AS ps ON pt.PointID = ps.PointID
	WHERE
(UnitOfMeasureID  = '48')
AND (  PointName LIKE '%ADX:WATT%')
)
--AND UTCDateTime <= GETUTCDATE() AND UTCDateTime >= DATEADD(day, -1, GETUTCDATE())
