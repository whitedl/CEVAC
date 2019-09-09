<?php
include "../functions.php";
foreach($_POST['fd'] as $i){
  if($i['name'] == "BuildingSName") $BuildingSName = $i['value'];
  if($i['name'] == "Metric") $Metric = $i['value'];
}
$RemotePSIDName = CEVAC_CONFIG_value('RemotePSIDName');
$RemotePointNameName = CEVAC_CONFIG_value('RemotePointNameName');
$RemoteUnitOfMeasureIDName = CEVAC_CONFIG_value('RemoteUnitOfMeasureIDName');

if(empty($RemotePSIDName)) die('Missing RemotePSIDName');
if(empty($RemotePointNameName)) die('Missing RemotePointNameName');
if(empty($RemoteUnitOfMeasureIDName)) die('Missing RemoteUnitOfMeasureName');

$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
for($i = 0; $i < sizeof($_POST['headers']); $i++){
  if($_POST['headers'][$i] == $RemotePSIDName) $PSID_c = $i;
  if($_POST['headers'][$i] == $RemotePointNameName) $PN_c = $i;
  if($_POST['headers'][$i] == "Alias") $Alias_c = $i;
  if($_POST['headers'][$i] == $RemoteUnitOfMeasureIDName) $UM_c = $i;
}

$query = "
DECLARE @A NVARCHAR(MAX);
DROP TABLE $PXREF;
CREATE TABLE $PXREF(
  $RemotePSIDName INT,
  $RemotePointNameName NVARCHAR(MAX),
  Alias NVARCHAR(MAX),
  $RemoteUnitOfMeasureIDName INT
); 
";
$insert_subquery = "
INSERT INTO $PXREF($RemotePSIDName, $RemotePointNameName, Alias, $RemoteUnitOfMeasureIDName)
VALUES(
";
$insert_subquery_end = "
);
";

// var_dump($_POST['tdata']);
for($i = 0; $i < sizeof($_POST['tdata']); $i++){
  $row = $_POST['tdata'][$i];
  $PSID = $row[$PSID_c];
  $PN = $row[$PN_c];
  $Alias = str_replace(array("\\r", "\\n", "<br>"), '', $row[$Alias_c]);
  $UM = $row[$UM_c];

  $query .= $insert_subquery.$PSID.",'".$PN."','";
  $query .= $Alias."',".$UM;
  $query .= $insert_subquery_end;

  $query .= "
  SET @A = NULL;
  IF OBJECT_ID('$XREF') IS NOT NULL SET @A = (SELECT TOP 1 Alias FROM $XREF WHERE $RemotePSIDName = $PSID ORDER BY UTCDateTime DESC);
  IF(@A != '$Alias' AND @A IS NOT NULL) BEGIN
    UPDATE $XREF
    SET Alias = '".$Alias."'
    WHERE $RemotePSIDName = $PSID;

    INSERT INTO CEVAC_ALIAS_LOG(PointSliceID, Alias, UTCDateTime)
    VALUES(
      $PSID,
      '$Alias',
      GETUTCDATE()
    );
  END
  ";

}
exec_sql($query);
?>
