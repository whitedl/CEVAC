IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_POWER_EMERGENCY_HIST'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_WATT_POWER_EMERGENCY_HIST
END
GO

CREATE VIEW CEVAC_WATT_POWER_EMERGENCY_HIST
AS

WITH original AS (
	SELECT 'Building Emergency' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
	FROM CEVAC_WATT_POWER_RAW_HIST
	WHERE Alias IN
	(
		SELECT Alias FROM CEVAC_WATT_POWER_XREF
		WHERE (Type = 'Emergency')
	) GROUP BY UTCDateTime
)
SELECT *, DATEPART(year, ETDateTime) AS Year, DATEPART(month, ETDateTime) AS Month, DATEPART(day, ETDateTime) AS Day
FROM original