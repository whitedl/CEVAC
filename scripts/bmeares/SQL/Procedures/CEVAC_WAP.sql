IF EXISTS(SELECT 1 FROM sys.procedures WHERE Name = 'CEVAC_WAP') DROP PROCEDURE CEVAC_WAP;
GO
CREATE PROCEDURE CEVAC_WAP @BuildingSName NVARCHAR(MAX), @Metric NVARCHAR(MAX), @execute BIT = 1
AS

DECLARE @error NVARCHAR(MAX);
DECLARE @ProcessName NVARCHAR(MAX);
SET @ProcessName = OBJECT_NAME(@@PROCID);

DECLARE @Create_HIST NVARCHAR(MAX);
DECLARE @Create_RAW NVARCHAR(MAX);

DECLARE @HIST NVARCHAR(MAX);
DECLARE @HIST_VIEW NVARCHAR(MAX);
DECLARE @HIST_RAW NVARCHAR(MAX);
SET @HIST = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST';
SET @HIST_VIEW = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST_VIEW';
SET @HIST_RAW = 'CEVAC_' + @BuildingSName + '_' + @Metric + '_HIST_RAW';

DECLARE @DateTimeName NVARCHAR(MAX);
DECLARE @IDName NVARCHAR(MAX);
DECLARE @AliasName NVARCHAR(MAX);
DECLARE @DataName NVARCHAR(MAX);

-- Verify @HIST_RAW does not exist
IF OBJECT_ID(@HIST_RAW) IS NOT NULL BEGIN
--    SET @error = @HIST_RAW + ' already exists';
--    EXEC CEVAC_LOG_ERROR @ErrorMessage = @error, @ProcessName = @ProcessName, @TableName = @HIST_RAW;
--    RAISERROR(@error, 11, 1);
--    RETURN
    SET @Create_RAW = '';
--    RETURN
END


------------------------
-- WAP
------------------------
IF @Metric = 'WAP' BEGIN
    IF @Create_RAW IS NULL BEGIN
        SET @Create_RAW = '
        CREATE TABLE ' + @HIST_RAW + '(
            time DATETIME,
            name NVARCHAR(MAX),
            ssid NVARCHAR(MAX),
            total_duration INT,
            predicted_occupancy FLOAT,
            unique_users INT
        );
        ';
    END
    SET @Create_HIST = '
		CREATE VIEW ' + @HIST_VIEW + ' AS
        SELECT time AS ''UTCDateTime'', dbo.ConvertUTCToLocal(time) AS ''ETDateTime'', name AS ''Alias'', ssid, total_duration, predicted_occupancy, unique_users
        FROM ' + @HIST_RAW + '
    ';
    SET @DateTimeName = 'UTCDateTime';
    SET @IDName = 'Alias';
    SET @AliasName = 'Alias';
    SET @DataName = 'unique_users';
 END

------------------------
-- WAP_DAILY
------------------------
IF @Metric = 'WAP_DAILY' BEGIN
    IF @Create_RAW IS NULL BEGIN
        SET @Create_RAW = '
        CREATE TABLE ' + @HIST_RAW + '(
            UTCDateTime DATETIME,
            clemson_count INT,
            guest_count INT
        );
        ';
    END
    SET @Create_HIST = '
	CREATE VIEW ' + @HIST_VIEW + ' AS
    WITH original AS (
        SELECT * FROM ' + @HIST_RAW + '
    ) SELECT *, (clemson_count + guest_count) AS ''total_count''
    FROM ' + @HIST_RAW + '
    ';
    SET @DateTimeName = 'UTCDateTime';
    SET @IDName = 'UTCDateTime';
    SET @AliasName = 'UTCDateTime';
    SET @DataName = 'total_count';

END

------------------------
-- WAP_FLOOR
------------------------
IF @Metric = 'WAP_FLOOR' BEGIN
    IF @Create_RAW IS NULL BEGIN
        SET @Create_RAW = '
            CREATE TABLE ' + @HIST_RAW + '(
                UTCDateTime DATETIME,
                floor INT,
                guest_count INT,
                clemson_count INT
            );
        ';
    END
    SET @Create_HIST = '
	CREATE VIEW ' + @HIST_VIEW + ' AS
    SELECT UTCDateTime, dbo.ConvertUTCToLocal(UTCDateTime) AS ''ETDateTime'', floor, guest_count, clemson_count, (guest_count + clemson_count) AS ''total_count''
    FROM ' + @HIST_RAW + '
    ';
    SET @DateTimeName = 'UTCDateTime';
    SET @IDName = 'floor';
    SET @AliasName = 'floor';
    SET @DataName = 'total_count';
END


-- insert into CEVAC_TABLES for CEVAC_CUSTOM to grab definition
DELETE FROM CEVAC_TABLES WHERE TableName = @HIST_VIEW;
INSERT INTO CEVAC_TABLES(BuildingSName, Metric, Age, TableName, DateTimeName, IDName, AliasName, DataName, isCustom, Definition, Dependencies, customLASR, autoCACHE, autoLASR) VALUES (
        @BuildingSName,
        @Metric,
        'HIST',
        @HIST_VIEW,
        @DateTimeName,
        @IDName,
        @AliasName,
        @DataName,
        1,
        @Create_HIST,
        @HIST_RAW,
        0,
        1,
        0
    );

IF @execute = 1 BEGIN
    EXEC(@Create_RAW);
    IF OBJECT_ID(@HIST_VIEW) IS NOT NULL BEGIN
        EXEC('DROP VIEW ' + @HIST_VIEW);
    END
    EXEC CEVAC_CUSTOM_HIST @BuildingSName = @BuildingSName, @Metric = @Metric;
    EXEC CEVAC_VIEW @Building = @BuildingSName, @Metric = @Metric, @Age = 'HIST';
    EXEC CEVAC_VIEW @Building = @BuildingSName, @Metric = @Metric, @Age = 'DAY';
    EXEC CEVAC_VIEW @Building = @BuildingSName, @Metric = @Metric, @Age = 'LATEST';
END