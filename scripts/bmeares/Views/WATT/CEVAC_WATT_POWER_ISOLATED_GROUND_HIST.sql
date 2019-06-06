IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_POWER_ISOLATED_GROUND_HIST'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_WATT_POWER_ISOLATED_GROUND_HIST
END
GO

CREATE VIEW CEVAC_WATT_POWER_ISOLATED_GROUND_HIST
AS


SELECT 'Building Isolated Ground' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue, DATEPART(year, UTCDateTime) AS Year, DATEPART(month, UTCDateTime) AS Month, DATEPART(day, UTCDateTime) AS Day
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Type = 'Isolated Ground')
)
AND UTCDateTime <= GETUTCDATE() AND UTCDateTime >= DATEADD(day, -1, GETUTCDATE())
GROUP BY UTCDateTime
