SELECT UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', SUM(ActualValue) AS 'Total_Usage'
FROM CEVAC_WATT_POWER_HIST AS ph
INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = ph.PointSliceID
INNER JOIN CEVAC_WATT_POWER_QUORUM AS q ON q.agg_name = 'Floor' AND q.agg_key = x.Floor AND ph.UTCDateTime >= q.begin_UTC AND ph.UTCDateTime < q.end_UTC
WHERE x.Floor = 'Building'
GROUP BY UTCDateTime, q.PSID_count
HAVING q.PSID_count <= COUNT(ph.PointSliceID)
