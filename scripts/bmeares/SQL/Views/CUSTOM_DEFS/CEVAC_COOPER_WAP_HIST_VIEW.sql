WITH r AS (
  SELECT time, name, ssid, total_duration, predicted_occupancy, unique_users
  FROM CEVAC_COOPER_WAP_HIST_RAW
)
SELECT r.time AS 'UTCDateTime', dbo.ConvertUTCToLocal(r.time) AS 'ETDateTime', r.name AS 'Alias', r.ssid AS 'ssid',
r.total_duration AS 'total_duration', r.predicted_occupancy AS 'predicted_occupancy', r.unique_users AS 'unique_users'
FROM r
