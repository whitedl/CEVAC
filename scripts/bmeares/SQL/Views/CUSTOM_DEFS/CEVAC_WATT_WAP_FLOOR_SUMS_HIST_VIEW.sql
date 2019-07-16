WITH original AS (
	SELECT * FROM CEVAC_WATT_WAP_FLOOR_HIST
), sums AS (
	SELECT UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS 'ETDateTime', SUM(guest_count) AS 'SUM_guest_count', SUM(clemson_count) AS 'SUM_clemson_count'
	FROM original
	GROUP BY UTCDateTime
)
SELECT *, (SUM_guest_count + SUM_clemson_count) AS 'SUM_total' FROM sums



