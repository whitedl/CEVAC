IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_WAP_VISITORS_HIST'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_WATT_WAP_VISITORS_HIST
END
GO
CREATE VIEW CEVAC_WATT_WAP_VISITORS_HIST AS
SELECT time, 'Building visitors' AS Alias, 'VISITORS' AS ssid, SUM(total_duration) AS total_duration, SUM(predicted_occupancy) AS predicted_occupancy, SUM(unique_users) AS unique_users
FROM CEVAC_WATT_WAP_HIST_RAW
WHERE ssid = 'eduroam' OR ssid = 'clemsonguest'
GROUP BY time
