SET NOCOUNT ON
DECLARE @begin DATETIME;
SET @begin = (SELECT TOP 1 UTCDateTime FROM CEVAC_WATT_WAP_FLOOR_OLDEST ORDER BY UTCDateTime ASC);
DECLARE @results TABLE(UTCDateTime DATETIME, floor_int INT, temperature FLOAT, power FLOAT, occupancy INT, table_int INT);
DECLARE @with_occupancy TABLE(UTCDateTime DATETIME, floor_int INT, temperature FLOAT, power FLOAT, occupancy INT);
DECLARE @without_occupancy TABLE(UTCDateTime DATETIME, floor_int INT, temperature FLOAT, power FLOAT, occupancy INT);
DECLARE @dataset TABLE(UTCDateTime DATETIME, hour INT, weekday INT, floor_int INT, temperature FLOAT, power FLOAT, occupancy INT);

DECLARE @new_power_sums TABLE (PointSliceID INT, Alias NVARCHAR(MAX), UTCDateTime DATETIME, ActualValue FLOAT, floor_int INT);
DECLARE @temp_all TABLE (PointSliceID INT, Alias NVARCHAR(MAX), UTCDateTime DATETIME, ActualValue FLOAT, floor_int INT);
DECLARE @all_avg_temp TABLE(UTCDateTime DATETIME, temperature FLOAT, floor_int INT);
DECLARE @new_temp TABLE(UTCDateTime DATETIME, temperature FLOAT, floor_int INT);
--DECLARE @with_occupancy TABLE(UTCDateTime DATETIME, floor_int INT, temperature FLOAT, power FLOAT, occupancy INT);

-------------------------------
-- Power data by floor (using pre-aggregated artificial sensors)
-------------------------------
WITH new_power_sums AS (
    SELECT h.PointSliceID, h.Alias, h.UTCDateTime, h.ActualValue, CASE
        WHEN x.floor = 'Basement' THEN 0
        WHEN x.floor = '1st Floor' THEN 1
        WHEN x.floor = '2nd Floor' THEN 2
        WHEN x.floor = '3rd Floor' THEN 3
        WHEN x.floor = '4th Floor' THEN 4
        WHEN x.floor = 'Building' THEN 5
        ELSE NULL
    END AS floor_int
    FROM CEVAC_WATT_POWER_HIST AS h
    INNER JOIN CEVAC_WATT_POWER_XREF AS x ON x.PointSliceID = h.PointSliceID
    -----------------------------------------------------------------------------------------
    -- Only include floor sums (negative PSIDs), Media Lights and HVAC (for 'Building' floor)
    -----------------------------------------------------------------------------------------
    WHERE x.PointSliceID IN (-7, -6,-5, -4, -3, -2, 23303, 21461)
    AND UTCDateTime > @begin
) INSERT INTO @new_power_sums SELECT * FROM new_power_sums;
-------------------------------
-- All temperature data (with floor as int)
-------------------------------
WITH temp_all AS (
    SELECT h.PointSliceID, h.Alias, h.UTCDateTime, h.ActualValue, CASE
        WHEN x.floor = 'Basement' THEN 0
        WHEN x.floor = '1st Floor' THEN 1
        WHEN x.floor = '2nd Floor' THEN 2
        WHEN x.floor = '3rd Floor' THEN 3
        WHEN x.floor = '4th Floor' THEN 4
        WHEN x.floor = 'Building' THEN 5
        ELSE NULL
    END AS floor_int
    FROM CEVAC_WATT_TEMP_HIST AS h
    INNER JOIN CEVAC_WATT_TEMP_XREF AS x ON x.PointSliceID = h.PointSliceID
    AND UTCDateTime > @begin
) INSERT INTO @temp_all SELECT * FROM temp_all;
-------------------------------
-- Average temperature for the entire building
-------------------------------
WITH all_avg_temp AS (
    SELECT UTCDateTime, AVG(ActualValue) AS 'temperature', 5 AS 'floor_int'
    FROM @temp_all
    GROUP BY UTCDateTime
) INSERT INTO @all_avg_temp SELECT * FROM all_avg_temp;
-------------------------------
-- Average temperature by floor
-------------------------------
WITH new_temp AS (
    SELECT UTCDateTime, AVG(ActualValue) AS 'temperature', floor_int
    FROM @temp_all
    GROUP BY floor_int, UTCDateTime
) INSERT INTO @new_temp SELECT * FROM new_temp;
-------------------------------
-- INNER JOIN power and temp with occupancy data
-------------------------------
WITH with_occupancy AS (
    SELECT ps.UTCDateTime, ps.floor_int, t.temperature, ps.ActualValue AS 'power', wf.total_count AS 'occupancy'
    FROM @new_power_sums AS ps
    INNER JOIN @new_temp AS t ON t.floor_int = ps.floor_int AND t.UTCDateTime = ps.UTCDateTime
    INNER JOIN CEVAC_WATT_WAP_FLOOR_HIST AS wf ON CAST(wf.floor AS INT) = ps.floor_int AND wf.UTCDateTime = ps.UTCDateTime
) INSERT INTO @with_occupancy SELECT * FROM with_occupancy;
-------------------------------
-- INNER JOIN power and temp without occupancy data (for 'floor 5')
-------------------------------
WITH without_occupany AS (
    SELECT ps.UTCDateTime, ps.floor_int, t.temperature, ps.ActualValue AS 'power', 0 AS 'occupancy'
    FROM @new_power_sums AS ps
    INNER JOIN @all_avg_temp AS t ON t.floor_int = ps.floor_int AND t.UTCDateTime = ps.UTCDateTime
    -------------------------------
    -- Only include UTCDateTime that corresponds with datetimes with occupancy (prevent bias)
    -------------------------------
    INNER JOIN @with_occupancy AS wo ON wo.UTCDateTime = ps.UTCDateTime
) INSERT INTO @without_occupancy SELECT * FROM without_occupany;


INSERT INTO @dataset
SELECT o.UTCDateTime, DATEPART(HOUR, o.UTCDateTime) AS hour, DATEPART(WEEKDAY, o.UTCDateTime) AS weekday, o.floor_int, o.temperature, o.power, o.occupancy
FROM @with_occupancy AS o

INSERT INTO @dataset
SELECT o.UTCDateTime, DATEPART(HOUR, o.UTCDateTime) AS hour, DATEPART(WEEKDAY, o.UTCDateTime) AS weekday, o.floor_int, o.temperature, o.power, o.occupancy
FROM @without_occupancy AS o


IF OBJECT_ID('RESULTS_TEMPORARY') IS NOT NULL DROP TABLE RESULTS_TEMPORARY;
SELECT *
INTO RESULTS_TEMPORARY
FROM @dataset
