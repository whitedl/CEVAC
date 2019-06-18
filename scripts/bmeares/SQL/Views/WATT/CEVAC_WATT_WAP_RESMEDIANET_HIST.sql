IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_WAP_RESMEDIANET_HIST'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_WATT_WAP_RESMEDIANET_HIST
END
GO
CREATE VIEW CEVAC_WATT_WAP_RESMEDIANET_HIST AS
SELECT time, 'Building resmedianet' AS Alias, ssid, SUM(total_duration) AS total_duration, SUM(predicted_occupancy) AS predicted_occupancy, SUM(unique_users) AS unique_users
FROM CEVAC_WATT_WAP_HIST_RAW
WHERE ssid = 'resmedianet'
GROUP BY time, ssid
