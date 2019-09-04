<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$query = "SELECT * FROM $PXREF";
$result = exec_sql($query);
$output = "
<tr>
  <th>PointSliceID</th>
  <th>Alias</th>
  <th>UnitOfMeasureID</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $output .= "
  <tr>
    <td>".$row['PointSliceID']."</td>
    <td>".$row['Alias']."</td>
    <td>".$row['UnitOfMeasureID']."</td>
  </tr>
  ";
}
echo $output;
?>
