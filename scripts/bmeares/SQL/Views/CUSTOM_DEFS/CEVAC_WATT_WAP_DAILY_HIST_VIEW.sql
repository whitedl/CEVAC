WITH original AS (
  SELECT * FROM CEVAC_WATT_WAP_DAILY_HIST_RAW
) SELECT *, (clemson_count + guest_count) AS 'total_count'
FROM original
