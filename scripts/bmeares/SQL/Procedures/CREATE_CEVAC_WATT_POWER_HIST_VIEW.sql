IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CREATE_CEVAC_WATT_POWER_HIST_VIEW') DROP PROCEDURE CREATE_CEVAC_WATT_POWER_HIST_VIEW;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CREATE_CEVAC_WATT_POWER_HIST_VIEW
	@output NVARCHAR(MAX) OUTPUT
AS
DELETE FROM CEVAC_TABLES WHERE TableName = 'CREATE_CEVAC_WATT_POWER_HIST';
INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName)
VALUES(
	'WATT',
	'POWER',
	'HIST',
	'CREATE_CEVAC_WATT_POWER_HIST',
	'UTCDateTime',
	'Alias'
)

SET @output = '
CREATE VIEW CEVAC_WATT_POWER_HIST_VIEW AS
WITH CEVAC_WATT_POWER_EMERGENCY_HIST AS (
SELECT ''Building Emergency'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Type = ''Emergency'')
) GROUP BY UTCDateTime
),
CEVAC_WATT_POWER_ISOLATED_GROUND_HIST AS (
SELECT ''Building Isolated Ground'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Type = ''Isolated Ground'')
) GROUP BY UTCDateTime
),
CEVAC_WATT_POWER_1ST_FLOOR_HIST AS (
SELECT ''1st Floor Total'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Floor = ''1st Floor'')
) GROUP BY UTCDateTime
),
CEVAC_WATT_POWER_2ND_FLOOR_HIST AS (
SELECT ''2nd Floor Total'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Floor = ''2nd Floor'')
) GROUP BY UTCDateTime
),
CEVAC_WATT_POWER_3RD_FLOOR_HIST AS (
SELECT ''3rd Floor Total'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Floor = ''3rd Floor'')
) GROUP BY UTCDateTime
),
CEVAC_WATT_POWER_4TH_FLOOR_HIST AS (
SELECT ''4th Floor Total'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Floor = ''4th Floor'')
) GROUP BY UTCDateTime
),
CEVAC_WATT_POWER_BASEMENT_HIST AS (
SELECT ''Basement Total'' AS Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS ActualValue
FROM CEVAC_WATT_POWER_RAW_HIST
WHERE Alias IN
(
	SELECT Alias FROM CEVAC_WATT_POWER_XREF
	WHERE (Floor = ''Basement'')
) GROUP BY UTCDateTime
)

SELECT * FROM CEVAC_WATT_POWER_RAW_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_EMERGENCY_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_ISOLATED_GROUND_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_1ST_FLOOR_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_2ND_FLOOR_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_3RD_FLOOR_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_4TH_FLOOR_HIST
UNION
SELECT * FROM
CEVAC_WATT_POWER_BASEMENT_HIST
';