WITH all_utc AS (
	SELECT UTCDateTime, COUNT(UTCDateTime) AS UTCCount FROM CEVAC_WATT_POWER_HIST
	WHERE Alias LIKE 'Building%'
	GROUP BY UTCDateTime
), original AS (
	SELECT UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime, SUM(ActualValue) AS Total_Usage
	FROM
	(SELECT * FROM CEVAC_WATT_POWER_HIST
	 WHERE Alias LIKE 'Building%'
	 AND UTCDateTime IN (SELECT UTCDateTime FROM all_utc)
	 ) AS Building
	GROUP BY UTCDateTime
)
SELECT *
FROM original
