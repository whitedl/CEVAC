WITH Aggregated AS (
	SELECT Jonathan.UTCDateTime AS 'P_UTCDateTime', Reality.UTCDateTime AS 'UTCDateTime', 
		Jonathan.ETDateTime AS 'P_ETDateTime', Reality.ETDateTime AS 'ETDateTime',
		Jonathan.Total_Usage AS 'P_Total_Usage', Reality.Total_Usage AS 'Total_Usage'
	FROM CEVAC_WATT_POWER_SUMS_PRED_HIST_RAW AS Jonathan
	LEFT JOIN CEVAC_WATT_POWER_SUMS_HIST AS Reality
		ON Jonathan.UTCDateTime = Reality.UTCDateTime
)
SELECT *, P_Total_Usage - Total_Usage AS 'Difference', ABS(P_Total_Usage - Total_Usage) AS 'Absolute_Error'
FROM Aggregated

