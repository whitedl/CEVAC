IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_POWER_SUMS_COMPARE_HIST_VIEW'
AND TABLE_TYPE ='VIEW')
BEGIN
DROP VIEW CEVAC_WATT_POWER_SUMS_COMPARE_HIST_VIEW
END
GO
DELETE FROM CEVAC_TABLES WHERE TableName = 'CEVAC_WATT_POWER_SUMS_COMPARE_HIST';
INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName)
VALUES(
	'WATT',
	'POWER_SUMS_COMPARE',
	'HIST',
	'CEVAC_WATT_POWER_SUMS_COMPARE_HIST',
	'P_UTCDateTime',
	'P_Total_Usage'
)


GO

CREATE VIEW CEVAC_WATT_POWER_SUMS_COMPARE_HIST_VIEW AS
WITH Aggregated AS (
	SELECT Jonathan.UTCDateTime AS 'P_UTCDateTime', Reality.UTCDateTime AS 'UTCDateTime', 
		Jonathan.ETDateTime AS 'P_ETDateTime', Reality.ETDateTime AS 'ETDateTime',
		Jonathan.Total_Usage AS 'P_Total_Usage', Reality.Total_Usage AS 'Total_Usage'
	FROM CEVAC_WATT_POWER_SUMS_PRED_HIST_RAW AS Jonathan
	LEFT JOIN CEVAC_WATT_POWER_SUMS_HIST_VIEW AS Reality
		ON Jonathan.UTCDateTime = Reality.UTCDateTime
	--	AND Jonathan.ETDateTime = Reality.ETDateTime

)
SELECT *, P_Total_Usage - Total_Usage AS 'Absolute Error'
FROM Aggregated
--ORDER BY P_UTCDateTime ASC

