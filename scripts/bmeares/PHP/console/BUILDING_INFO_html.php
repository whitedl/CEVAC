<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$query = "
  SELECT BuildingSName, BuildingDName, BuildingKey, ReportLink
  FROM CEVAC_BUILDING_INFO AS bi
  ORDER BY BuildingSName ASC
";
$result = exec_sql($query);
$output = "
<tr>
  <th>BuildingSName</th>
  <th>BuildingDName</th>
  <th>BuildingKey</th>
  <th>ReportLink</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $output .= "
  <tr>
    <td contenteditable='true'>".$row['BuildingSName']."</td>
    <td contenteditable='true'>".$row['BuildingDName']."</td>
    <td contenteditable='true'>".$row['BuildingKey']."</td>
    <td contenteditable='true'>".$row['ReportLink']."</td>
  </tr>
  ";
}
echo $output;
?>
