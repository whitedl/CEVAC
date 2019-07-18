IF OBJECT_ID('CEVAC_TABLES_RECORDS_COMPARE') IS NOT NULL DROP VIEW CEVAC_TABLES_RECORDS_COMPARE;
GO
CREATE VIEW CEVAC_TABLES_RECORDS_COMPARE
AS

WITH cache_max AS (
	SELECT MAX(update_time) AS max_utc, table_name FROM CEVAC_CACHE_RECORDS
	GROUP BY table_name
),
cache_newest AS (
	SELECT * FROM CEVAC_CACHE_RECORDS AS c
	WHERE update_time = (SELECT max_utc FROM cache_max WHERE c.table_name = cache_max.table_name)
)

SELECT * FROM CEVAC_TABLES AS t
INNER JOIN cache_newest ON cache_newest.table_name = t.TableName

--SELECT * FROM CEVAC_TABLES