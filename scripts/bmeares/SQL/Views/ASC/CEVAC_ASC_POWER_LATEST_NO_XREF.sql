IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME='CEVAC_ASC_POWER_LATEST'
AND TABLE_TYPE ='VIEW')
BEGIN
-- If the view exists, the code in this block will run.
DROP VIEW CEVAC_ASC_POWER_LATEST
END
GO


CREATE VIEW CEVAC_ASC_POWER_LATEST AS
(
	SELECT
	--temp.Alias,
	-- NOTE: Uncomment the above line and comment out the next once XREF is available for ASC_TEMP
	temp.PointSliceID,
	temp.UTCDateTime, temp.ActualValue, temp.Year, temp.Month, temp.Day FROM CEVAC_ASC_POWER_DAY AS temp
	INNER JOIN
	(
		SELECT
		PointSliceID,
--		Alias,
		MAX(UTCDateTime) AS LastTime
		FROM CEVAC_ASC_POWER_DAY
--		GROUP BY Alias
		GROUP BY PointSliceID

	) AS recent
	ON
	temp.PointSliceID = recent.PointSliceID
--	NOTE: Uncomment below later
--	temp.Alias = recent.Alias
	AND temp.UTCDateTime = recent.LastTime
)