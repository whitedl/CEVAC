WITH original AS (
	SELECT * FROM CEVAC_WATT_WAP_FLOOR_HIST
),
floor_distinct AS (
	SELECT DISTINCT floor FROM original
),
floor_count AS(
	SELECT COUNT(*) AS count FROM floor_distinct
),
freq AS (
	SELECT COUNT(UTCDateTime) AS 'count', UTCDateTime FROM CEVAC_WATT_WAP_FLOOR_HIST AS h
	GROUP BY UTCDateTime
),
filtered_utc AS (
	SELECT UTCDateTime FROM freq
	WHERE count = (SELECT TOP 1 count FROM floor_count)
), sums AS (
	SELECT UTCDateTime, SUM(guest_count) AS 'SUM_guest_count', SUM(clemson_count) AS 'SUM_clemson_count'
	 FROM original
	WHERE UTCDateTime IN (SELECT UTCDateTime FROM filtered_utc)
	GROUP BY UTCDateTime
) SELECT *, (SUM_guest_count + SUM_clemson_count) AS 'SUM_total' FROM sums


