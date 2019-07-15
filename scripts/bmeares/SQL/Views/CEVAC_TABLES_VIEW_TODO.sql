WITH R_Latest AS (
	SELECT table_name, MAX(update_time) AS 'update_time' FROM CEVAC_CACHE_RECORDS
	GROUP BY table_name
)

SELECT T.*, R.update_time FROM CEVAC_TABLES AS T
INNER JOIN R_Latest ON T.TableName = R_Latest.table_name
