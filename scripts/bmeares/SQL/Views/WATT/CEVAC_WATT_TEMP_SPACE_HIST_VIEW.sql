WITH aliases AS (
	SELECT Alias FROM CEVAC_WATT_TEMP_XREF
	WHERE RoomType IN (
		'Breakroom','Classroom','Comm Studio','Kitchen','Office','Project Room'
	) AND ReadingType = 'Temp'
) SELECT * FROM CEVAC_WATT_TEMP_LATEST AS l WHERE l.Alias IN (SELECT * FROM aliases);

