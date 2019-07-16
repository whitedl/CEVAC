WITH LatestTimes AS (
	SELECT EventID, MAX(UTCDateTime) AS 'maxUTC'
	FROM CEVAC_ALL_ALERTS_HIST_RAW
	GROUP BY EventID
), DetectTimes AS (
	SELECT EventID, MIN(UTCDateTime) AS 'minUTC'
	FROM CEVAC_ALL_ALERTS_HIST_RAW
	GROUP BY EventID
)
SELECT AlertType, AlertMessage, Metric, BuildingSName, BuildingDName, Acknowledged, Raw.EventID, dbo.ConvertUTCToLocal(LatestTimes.maxUTC) AS 'ETDateTime', dbo.ConvertUTCToLocal(DetectTimes.minUTC) AS 'DetectionTimeET'
FROM CEVAC_ALL_ALERTS_HIST_RAW AS Raw
INNER JOIN LatestTimes ON LatestTimes.EventID = Raw.EventID AND LatestTimes.maxUTC = Raw.UTCDateTime
INNER JOIN DetectTimes ON DetectTimes.EventID = Raw.EventID
