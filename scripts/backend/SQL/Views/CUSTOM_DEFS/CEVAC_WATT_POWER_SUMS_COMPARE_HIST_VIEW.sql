WITH Aggregated AS (
	SELECT Jonathan.UTCDateTime AS 'P_UTCDateTime', Reality.UTCDateTime AS 'UTCDateTime', 
		Jonathan.ETDateTime AS 'P_ETDateTime', Reality.ETDateTime AS 'ETDateTime',
		Jonathan.Total_Usage AS 'P_Total_Usage', Reality.ActualValue AS 'Total_Usage'
	FROM CEVAC_WATT_POWER_SUMS_PRED_HIST_RAW AS Jonathan
	LEFT OUTER JOIN CEVAC_WATT_POWER_SUMS_HIST AS Reality
		ON Jonathan.UTCDateTime = Reality.UTCDateTime
), subs AS (
	SELECT P_UTCDateTime, UTCDateTime, P_ETDateTime, ETDateTime, P_Total_Usage, Total_Usage, P_Total_Usage - Total_Usage AS 'Difference', ABS(P_Total_Usage - Total_Usage) AS 'Absolute_Error'
	FROM Aggregated
), avg_d AS (
	SELECT AVG(Difference) AS 'AVG_Difference' FROM subs
) SELECT *, (P_Total_Usage  - (SELECT TOP 1 AVG_Difference FROM avg_d)) AS 'P_Total_Corrected' FROM subs


