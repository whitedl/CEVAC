<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$query = "
  SELECT p.PointSliceID AS 'PointSliceID', PointName AS 'PointName', p.UnitOfMeasureID AS 'UnitOfMeasureID', p.Alias AS 'Alias'
  FROM $PXREF AS p
  ORDER BY PointSliceID ASC
";
$result = exec_sql($query);
$output = "
<tr>
  <th>PointSliceID</th>
  <th>PointName</th>
  <th>Alias</th>
  <th>UnitOfMeasureID</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $output .= "
  <tr>
    <td>".$row['PointSliceID']."</td>
    <td>".$row['PointName']."</td>
    <td contenteditable='true'>".$row['Alias']."</td>
    <td>".$row['UnitOfMeasureID']."</td>
  </tr>
  ";
}
echo $output;
?>
