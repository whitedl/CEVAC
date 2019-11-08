<?php
include "../../functions.php";
// var_dump($_POST);
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$BuildingKey = clean($_GET['BuildingKey']);
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])
  || !isset($_GET['BuildingKey'])) die('missing params');
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
WHERE
pt.$RemotePointNameName LIKE '%$BuildingKey%'

";
$result = exec_sql($query);
$output = "
<tr>
  <th>$RemotePSIDName</th>
  <th>$RemotePointNameName</th>
  <th>$RemoteUnitOfMeasureNameName</th>
  <th>$RemoteUnitOfMeasureIDName</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $output .= "
  <tr>
    <td class='$class'>".$row[$RemotePSIDName]."</td>
    <td class='$class'>".$row[$RemotePointNameName]."</td>
    <td class='$class'>".$row[$RemoteUnitOfMeasureNameName]."</td>
    <td class='$class'>".$row[$RemoteUnitOfMeasureIDName]."</td>
  </tr>
  ";
}
echo $output;
?>
