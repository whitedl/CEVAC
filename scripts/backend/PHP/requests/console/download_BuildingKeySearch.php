<?php
include "../../functions.php";
// var_dump($_POST);

$BuildingKey = clean($_GET['BuildingKey']);
if(!isset($_GET['BuildingKey'])) die('Missing BuildingKey');
$RemoteIP = CEVAC_CONFIG_value('RemoteIP');
$RemoteDB = CEVAC_CONFIG_value('RemoteDB');
$RemoteSchema = CEVAC_CONFIG_value('RemoteSchema');
$RemotePSIDName = CEVAC_CONFIG_value('RemotePSIDName');
$RemotePointIDName = CEVAC_CONFIG_value('RemotePointIDName');
$RemotePSTable = CEVAC_CONFIG_value('RemotePSTable');
$RemotePtTable = CEVAC_CONFIG_value('RemotePtTable');
$RemoteUnitTable = CEVAC_CONFIG_value('RemoteUnitTable');
$RemotePointNameName = CEVAC_CONFIG_value('RemotePointNameName');
$RemoteUnitOfMeasureIDName = CEVAC_CONFIG_value('RemoteUnitOfMeasureIDName');
$RemoteUnitOfMeasureNameName = CEVAC_CONFIG_value('RemoteUnitOfMeasureNameName');

$query = "
SELECT ps.$RemotePSIDName, pt.$RemotePointNameName, um.$RemoteUnitOfMeasureNameName, um.$RemoteUnitOfMeasureIDName
FROM [$RemoteIP].[$RemoteDB].[$RemoteSchema].$RemotePSTable as ps
INNER JOIN [$RemoteIP].[$RemoteDB].[$RemoteSchema].$RemotePtTable as pt ON ps.$RemotePointIDName = pt.$RemotePointIDName
INNER JOIN [$RemoteIP].[$RemoteDB].[$RemoteSchema].$RemoteUnitTable as um on um.$RemoteUnitOfMeasureIDName = pt.$RemoteUnitOfMeasureIDName
WHERE pt.$RemotePointNameName LIKE '%$BuildingKey%'
";

$script = "sudo -u cevac /cevac/scripts/exec_sql.sh";
$fname = "BuildingKeySearch.csv";
$config = "\"$query\" \"$fname\"";
// Create CSV file
$output = `$script $config`;
`mv /cevac/cache/$fname /srv/csv/$fname`;
echo "csv/$fname";
?>
