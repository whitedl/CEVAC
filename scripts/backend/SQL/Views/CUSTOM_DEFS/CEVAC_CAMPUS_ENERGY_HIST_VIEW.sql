WITH aliases AS (
  SELECT DISTINCT Alias FROM CEVAC_CAMPUS_ENERGY_HIST_RAW
),
t_ids AS (
  SELECT *, DENSE_RANK() OVER(PARTITION BY Alias ORDER BY ETDateTime) AS T_ID FROM CEVAC_CAMPUS_ENERGY_HIST_RAW
), change AS (
	SELECT t1.ETDateTime, t1.ActualValue, t1.ActualValue - t2.ActualValue AS Change, t2.ETDateTime AS 'BeginET', CAST(DATEDIFF(MINUTE, t2.ETDateTime, t1.ETDateTime) AS FLOAT) / CAST(60 AS FLOAT) AS 'hour_offset', t1.Alias
	FROM t_ids AS t1
	INNER JOIN t_ids AS t2 ON t1.T_ID = t2.T_ID + 1 AND t1.Alias = t2.Alias
) SELECT (Change / hour_offset) AS 'Rate',* FROM change
