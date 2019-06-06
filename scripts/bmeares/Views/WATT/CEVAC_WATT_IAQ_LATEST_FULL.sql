IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_WATT_IAQ_LATEST_FULL'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_WATT_IAQ_LATEST_FULL
END
GO


CREATE VIEW CEVAC_WATT_IAQ_LATEST_FULL AS
(
	SELECT
	temp.Alias,
	-- NOTE: Uncomment the above line and comment out the next once XREF is available for ASC_TEMP
	--temp.PointSliceID,
	temp.UTCDateTime, temp.ActualValue, temp.Year, temp.Month, temp.Day FROM CEVAC_WATT_IAQ_HIST AS temp
	INNER JOIN
	(
		SELECT
--		PointSliceID,
		Alias,
		MAX(UTCDateTime) AS LastTime
		FROM CEVAC_WATT_IAQ_HIST
		GROUP BY Alias
--		GROUP BY PointSliceID

	) AS recent
	ON
--	temp.PointSliceID = recent.PointSliceID
--	NOTE: Uncomment below later
	temp.Alias = recent.Alias
	AND temp.UTCDateTime = recent.LastTime
)