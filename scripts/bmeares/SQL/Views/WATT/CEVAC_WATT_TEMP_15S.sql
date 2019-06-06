


CREATE VIEW CEVAC_WATT_TEMP_LATEST AS
(
	SELECT temp.Alias, temp.UTCDateTime, temp.ActualValue, temp.Year, temp.Month, temp.Day FROM CEVAC_WATT_TEMP_DAY AS temp
	INNER JOIN
	(
		SELECT Alias, MAX(UTCDateTime) AS LastTime
		FROM CEVAC_WATT_TEMP_DAY
		GROUP BY Alias

	) AS recent
	ON temp.Alias = recent.Alias AND temp.UTCDateTime = recent.LastTime
)