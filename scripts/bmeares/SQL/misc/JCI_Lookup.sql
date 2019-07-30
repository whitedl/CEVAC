USE JCIHistorianDB;
GO

SELECT PointSliceID, PointName, um.UnitOfMeasureName, um.UnitOfMeasureID FROM tblPointSlice as ps
INNER JOIN tblPoint as pt ON ps.PointID = pt.PointID
INNER JOIN tblUnitOfMeasure as um on um.UnitOfMeasureID = pt.UnitOfMeasureID

WHERE
PointName LIKE '%ADX:WATT%'
--AND PointName LIKE '%data-znt%'
AND um.UnitOfMeasureID = 19