WITH CEVAC_WATT_POWER_EMERGENCY_HIST AS (
	SELECT -1 AS PointSliceID, 'Building Emergency' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.ReadingType = 'Emergency'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
),
CEVAC_WATT_POWER_ISOLATED_GROUND_HIST AS (
	SELECT -2 AS PointSliceID, 'Building Isolated Ground' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.ReadingType = 'Isolated Ground'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
),
CEVAC_WATT_POWER_1ST_FLOOR_HIST AS (
	SELECT -3 AS PointSliceID, '1st Floor Total' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.Floor = '1st Floor'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
),
CEVAC_WATT_POWER_2ND_FLOOR_HIST AS (
	SELECT -4 AS PointSliceID, '2nd Floor Total' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.Floor = '2nd Floor'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
),
CEVAC_WATT_POWER_3RD_FLOOR_HIST AS (
	SELECT -3 AS PointSliceID, '3rd Floor Total' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.Floor = '3rd Floor'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
),
CEVAC_WATT_POWER_4TH_FLOOR_HIST AS (
	SELECT -3 AS PointSliceID, '4th Floor Total' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.Floor = '4th Floor'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
),
CEVAC_WATT_POWER_BASEMENT_HIST AS (
	SELECT -3 AS PointSliceID, 'Basement Total' AS Alias, UTCDateTime, SUM(ActualValue) AS ActualValue 
	FROM CEVAC_WATT_POWER_RAW_HIST AS h
	INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
	INNER JOIN CEVAC_WATT_POWER_RAW_QUORUM AS q ON q.agg_key = x.ReadingType AND h.UTCDateTime >= q.begin_UTC AND h.UTCDateTime < end_UTC
	WHERE x.Floor = 'Basement'
	GROUP BY UTCDateTime, q.PSID_count
	HAVING q.PSID_count = COUNT(ActualValue)
)
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_RAW_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_EMERGENCY_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_ISOLATED_GROUND_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_1ST_FLOOR_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_2ND_FLOOR_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_3RD_FLOOR_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_4TH_FLOOR_HIST
UNION
SELECT PointSliceID, Alias, UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', ActualValue FROM
CEVAC_WATT_POWER_BASEMENT_HIST
