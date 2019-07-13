IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CREATE_CEVAC_ALL_ALERTS_EVENTS_HIST_VIEW') DROP PROCEDURE CREATE_CEVAC_ALL_ALERTS_EVENTS_HIST_VIEW;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CREATE_CEVAC_ALL_ALERTS_EVENTS_HIST_VIEW
	@output NVARCHAR(MAX) OUTPUT
AS
DELETE FROM CEVAC_TABLES WHERE TableName = 'CEVAC_ALL_ALERTS_EVENTS_HIST';
INSERT INTO CEVAC_TABLES (BuildingSName, Metric, Age, TableName, DateTimeName, AliasName)
VALUES(
	'ALL',
	'ALERTS_EVENTS',
	'HIST',
	'CEVAC_ALL_ALERTS_EVENTS_HIST',
	'ETDateTime',
	'EventID'
)

SET @output = '
CREATE VIEW CEVAC_ALL_ALERTS_EVENTS_HIST_VIEW AS

WITH LatestTimes AS (
	SELECT EventID, MAX(UTCDateTime) AS ''maxUTC''
	FROM CEVAC_ALL_ALERTS_HIST_RAW
	GROUP BY EventID
), DetectTimes AS (
	SELECT EventID, MIN(UTCDateTime) AS ''minUTC''
	FROM CEVAC_ALL_ALERTS_HIST_RAW
	GROUP BY EventID
)
SELECT AlertType, AlertMessage, Metric, BuildingSName, BuildingDName, Acknowledged, Raw.EventID, dbo.ConvertUTCToLocal(LatestTimes.maxUTC) AS ''ETDateTime'', dbo.ConvertUTCToLocal(DetectTimes.minUTC) AS ''DetectionTimeET''
FROM CEVAC_ALL_ALERTS_HIST_RAW AS Raw
INNER JOIN LatestTimes ON LatestTimes.EventID = Raw.EventID AND LatestTimes.maxUTC = Raw.UTCDateTime
INNER JOIN DetectTimes ON DetectTimes.EventID = Raw.EventID

';