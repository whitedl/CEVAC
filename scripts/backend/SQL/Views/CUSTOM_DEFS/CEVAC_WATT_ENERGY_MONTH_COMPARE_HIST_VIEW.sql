WITH begins AS (
	SELECT
	temp.* FROM CEVAC_WATT_ENERGY_HIST AS temp
	INNER JOIN
	(
		SELECT PointSliceID, 
		MIN(ETDateTime) AS LastTime
		FROM
		CEVAC_WATT_ENERGY_HIST
		GROUP BY PointSliceID, DATEPART(MONTH, ETDateTime), DATEPART(YEAR, ETDateTime)
	) AS recent
	ON
	temp.PointSliceID = recent.PointSliceID
	AND temp.ETDateTime = recent.LastTime
),
ends AS (
	SELECT
	temp.* FROM CEVAC_WATT_ENERGY_HIST AS temp
	INNER JOIN
	(
		SELECT PointSliceID, 
		MAX(ETDateTime) AS LastTime
		FROM
		CEVAC_WATT_ENERGY_HIST
		GROUP BY PointSliceID, DATEPART(MONTH, ETDateTime), DATEPART(YEAR, ETDateTime)
	) AS recent
	ON
	temp.PointSliceID = recent.PointSliceID
	AND temp.ETDateTime = recent.LastTime
)

SELECT begins.PointSliceID, begins.Alias, begins.ETDateTime AS begin_ET, ends.ETDateTime AS end_ET, (ends.ActualValue - begins.ActualValue) AS ActualValue
FROM ends
INNER JOIN begins ON DATEPART(MONTH, begins.ETDateTime) = DATEPART(MONTH, ends.ETDateTime) AND begins.PointSliceID = ends.PointSliceID AND DATEPART(YEAR, begins.ETDateTime) = DATEPART(YEAR, ends.ETDateTime)
WHERE DATEDIFF(DAY, begins.ETDateTime, ends.ETDateTime) > 25