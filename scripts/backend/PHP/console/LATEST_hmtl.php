<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$LATEST = "CEVAC_$BuildingSName"."_$Metric"."_LATEST";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$query = "
  SELECT l.PointSliceID AS 'PointSliceID', l.Alias AS 'Alias', l.UTCDateTime AS 'UTCDateTime', l.ETDateTime AS 'ETDateTime', l.ActualValue AS 'ActualValue'
  FROM $LATEST AS l
  ORDER BY UTCDateTime DESC
";
$result = exec_sql($query);
$output = "
<tr>
  <th>Alias</th>
  <th>ETDateTime</th>
  <th>ActualValue</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $output .= "
  <tr>
    <td>".$row['Alias']."</td>
    <td>".$row['ETDateTime']."</td>
    <td>".$row['ActualValue']."</td>
  </tr>
  ";
}
echo $output;
?>
