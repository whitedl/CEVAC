IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_CUSTOM_HIST') DROP PROCEDURE CEVAC_CUSTOM_HIST;
GO
SET ANSI_NULLS, QUOTED_IDENTIFIER ON;
GO
CREATE PROCEDURE CEVAC_CUSTOM_HIST
	@BuildingSName NVARCHAR(300),
	@Metric NVARCHAR(300)
AS
DECLARE @error NVARCHAR(MAX);
DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);

DECLARE @HIST NVARCHAR(300);
DECLARE @HIST_VIEW NVARCHAR(300);
DECLARE @CREATEName NVARCHAR(MAX);
DECLARE @Create_Procedure_query NVARCHAR(MAX);
DECLARE @dependency NVARCHAR(300);
DECLARE @dependecy_query NVARCHAR(MAX);
DECLARE @Create_view_out NVARCHAR(MAX);
DECLARE @Dependencies_query NVARCHAR(MAX);
DECLARE @Definition NVARCHAR(MAX);
DECLARE @Dependencies_list NVARCHAR(MAX);
SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';
SET @HIST_VIEW =  @HIST + '_VIEW';
SELECT @HIST_VIEW AS 'HIST_VIEW';
IF NOT EXISTS(SELECT TOP 1 Definition FROM CEVAC_TABLES WHERE TableName = @HIST_VIEW) BEGIN
	SET @error = 'Missing Definition from CEVAC_TABLES. Run CREATE_CUSTOM.sh to resolve';
	EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @HIST_VIEW;
	RAISERROR(@error,11,1);
	RETURN
END ELSE BEGIN
	SET @Definition = (SELECT TOP 1 Definition FROM CEVAC_TABLES WHERE TableName = @HIST_VIEW);
END

SET @Dependencies_list = (SELECT TOP 1 Dependencies FROM CEVAC_TABLES WHERE TableName = @HIST_VIEW)

DECLARE @cevac_dep TABLE(dep NVARCHAR(MAX));
INSERT INTO @cevac_dep SELECT * FROM ListTable(@Dependencies_list);

SET @Dependencies_query = '';

DECLARE @i INT;
SET @i = 100;
WHILE (EXISTS(SELECT 1 FROM @cevac_dep) AND @i > 0) BEGIN
	SET @dependency = (SELECT TOP 1 * FROM @cevac_dep);
	DELETE TOP(1) FROM @cevac_dep;
	SET @dependecy_query = '
	IF OBJECT_ID(''' + RTRIM(@dependency) + ''') IS NULL BEGIN
		EXEC CEVAC_LOG_ERROR @ErrorMessage = ''' + RTRIM(@HIST) + ' requires ' + RTRIM(@dependency) + ''', @ProcessName = ''' + @ProcessName + ''', @TableName = ''' + RTRIM(@HIST) + ''';
		RAISERROR(''' + RTRIM(@HIST) + ' requires ' + RTRIM(@dependency) + ''', 11, 1);
		RETURN
	END
	';

	SET @Dependencies_query = @Dependencies_query + @dependecy_query;
	SET @i = @i - 1;
END

SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';
SET @HIST_VIEW = @HIST + '_VIEW';
SET @CREATEName = 'CREATE_' + @HIST_VIEW;

DECLARE @DROP_HIST_VIEW NVARCHAR(300);
SET @DROP_HIST_VIEW = 'IF OBJECT_ID(''' + RTRIM(@HIST_VIEW) + ''') IS NOT NULL DROP VIEW ' + RTRIM(@HIST_VIEW);
EXEC(@DROP_HIST_VIEW);

SET @Create_view_out = '
CREATE VIEW ' + @HIST_VIEW + ' AS
' + @Definition + '
';

SELECT @CREATEName AS 'CREATEName';
SELECT @Dependencies_query AS 'Dependencies_query';
SELECT @HIST_VIEW AS 'HIST_VIEW';
DECLARE @DropProcedure NVARCHAR(MAX);
SET @DropProcedure = '
IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = ''' + isnull(@CREATEName,'CREATEName ERROR') + ''') DROP PROCEDURE ' + isnull(@CREATEName,'CREATEName ERROR') + ';
';
SET @Create_Procedure_query = '
CREATE PROCEDURE ' + isnull(@CREATEName,'CREATEName ERROR') + '
	@Definition_OUT NVARCHAR(MAX) OUTPUT
AS
 ' + isnull(@Dependencies_query,'') + ' 
SET @Definition_OUT = (SELECT Definition FROM CEVAC_TABLES WHERE TableName = ''' + isnull(@HIST_VIEW,'@HIST_VIEW ERROR') + ''');
';


SELECT @DropProcedure AS 'DropProcedure';
SELECT @Create_Procedure_query AS 'Create Procedure';


EXEC(@DropProcedure);
EXEC(@Create_Procedure_query);
DECLARE @out NVARCHAR(MAX);
EXEC @CreateNAME @Definition_OUT = @out OUTPUT;
SELECT @out;