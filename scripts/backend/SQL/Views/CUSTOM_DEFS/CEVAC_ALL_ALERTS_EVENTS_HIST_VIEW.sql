SELECT r.*, dbo.ConvertUTCToLocal(r.latest_UTC) AS 'ETDateTime', dbo.ConvertUTCToLocal(r.begin_UTC) AS 'DetectionTimeET'
FROM CEVAC_ALL_ALERTS_EVENTS_HIST_RAW AS r
INNER JOIN CEVAC_BUILDING_INFO AS b ON b.BuildingSName = r.BuildingSName

