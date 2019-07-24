IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_XREF_LOOKUP') DROP PROCEDURE CEVAC_XREF_LOOKUP;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_XREF_LOOKUP
	@BuildingSName NVARCHAR(100),
	@Metric NVARCHAR(100),
	@Alias NVARCHAR(200) = NULL,
	@PointSliceID INT = NULL
AS
DECLARE @error NVARCHAR(1000);

IF @Alias IS NULL AND @PointSliceID IS NULL BEGIN
	SET @error = 'Provide an Alias or a PointSliceID';
	RAISERROR(@error,11,1);
	RETURN;
END

IF @Alias IS NOT NULL AND @PointSliceID IS NOT NULL BEGIN
	SET @error = 'Provide either an Alias or a PointSliceID (both are not null)';
	RAISERROR(@error,11,1);
	RETURN;
END

DECLARE @XREF NVARCHAR(300);
SET @XREF = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_XREF';
IF OBJECT_ID(@XREF) IS NULL BEGIN
	SET @error = @XREF + ' does not exist';
	RAISERROR(@error,11,1);
	RETURN;
END

DECLARE @EXEC_SQL NVARCHAR(MAX);
IF @Alias IS NULL BEGIN
	SET @EXEC_SQL = 'SELECT Alias FROM ' + @XREF + ' WHERE PointSliceID = ' + CAST(@PointSliceID AS NVARCHAR(100));
END
IF @PointSliceID IS NULL BEGIN
	SET @EXEC_SQL = 'SELECT PointSliceID FROM ' + @XREF + ' WHERE Alias = ''' + @Alias + '''';
END

EXEC(@EXEC_SQL);