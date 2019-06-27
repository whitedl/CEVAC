DECLARE @Table_name NVARCHAR(30);
SET @Table_name = 'CEVAC_WATT_WATER_XREF';

if exists (select * from sys.objects where name = @Table_name and type = 'u')
    EXEC('drop table ' + @Table_name)

CREATE TABLE CEVAC_WATT_WATER_XREF(
	PointSliceID INT,
	Room NVARCHAR(10),
	PointName NVARCHAR(100),
	BLDG NVARCHAR(10),
	ReadingType NVARCHAR(10),
	Alias NVARCHAR(30)
)

GO
INSERT INTO CEVAC_WATT_WATER_XREF(
	PointSliceID,
	Room,
	PointName,
	BLDG,
	ReadingType,
	Alias
) VALUES(
	45110,
	'Building',
	'ClemsonADX:WATT-CENTER/Programming.Water Metering.DOMESTIC-WATER-DAILY.#85',
	'WATT',
	'Water',
	'Domestic Water Meter'
)
GO
INSERT INTO CEVAC_WATT_WATER_XREF(
	PointSliceID,
	Room,
	PointName,
	BLDG,
	ReadingType,
	Alias
) VALUES(
	45109,
	'Outside',
	'ClemsonADX:WATT-CENTER/Programming.Water Metering.IRRIGATION-WATER-DAILY.#85',
	'WATT',
	'Water',
	'Irrigation Water Meter'
)
GO