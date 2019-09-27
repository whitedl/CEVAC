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
DECLARE @error NVARCHAR(MAX);
DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);
DECLARE @XREF NVARCHAR(MAX);
SET @XREF = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_XREF';
DECLARE @PXREF NVARCHAR(MAX);
SET @PXREF = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_PXREF';
DECLARE @XREF_source NVARCHAR(MAX);
SET @XREF_source = @XREF;

EXEC CEVAC_ACTIVITY @TableName = @XREF, @ProcessName = @ProcessName;

DECLARE @RemotePSIDName NVARCHAR(MAX);
SET @RemotePSIDName = (SELECT TOP 1 VarValue FROM CEVAC_CONFIG WHERE VarName = 'RemotePSIDName')

IF @Alias IS NULL AND @PointSliceID IS NULL BEGIN
	SET @error = 'Provide an Alias or a PointSliceID';
	EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @XREF;
	RAISERROR(@error,11,1);
	RETURN;
END

IF @Alias IS NOT NULL AND @PointSliceID IS NOT NULL BEGIN
	SET @error = 'Provide either an Alias or a ' + @RemotePSIDName + ' (both are not null)';
	EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @XREF;
	RAISERROR(@error,11,1);
	RETURN;
END

IF OBJECT_ID(@XREF) IS NULL BEGIN
	SET @XREF_source = @PXREF;
	IF OBJECT_ID(@PXREF) IS NULL BEGIN
		SET @error = @XREF + ' and ' + @PXREF + ' do not exist';
		EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @XREF;
		RAISERROR(@error,11,1);
		RETURN;
	END

END

DECLARE @EXEC_SQL NVARCHAR(MAX);
IF @Alias IS NULL BEGIN
	SET @EXEC_SQL = 'SELECT Alias FROM ' + @XREF_source + ' WHERE ' + @RemotePSIDName + ' = ' + CAST(@PointSliceID AS NVARCHAR(MAX));
END
IF @PointSliceID IS NULL BEGIN
	SET @EXEC_SQL = 'SELECT ' + @RemotePSIDName + ' FROM ' + @XREF_source + ' WHERE Alias = ''' + @Alias + '''';
END

EXEC(@EXEC_SQL);