WITH PSIDs AS (
	SELECT * FROM CEVAC_WATT_TEMP_XREF
	WHERE RoomType IN (
		'Breakroom','Classroom','Comm Studio','Kitchen','Office','Project Room'
	) AND ReadingType = 'Temp'
) 
SELECT l.* FROM CEVAC_WATT_TEMP_LATEST AS l 
INNER JOIN PSIDs AS p ON p.PointSliceID = l.PointSliceID

