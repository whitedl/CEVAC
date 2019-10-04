<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$query = "
  SELECT p.PointSliceID AS 'PointSliceID', PointName AS 'PointName',
  (CASE WHEN p.in_xref = 1 THEN 'True' ELSE 'False' END ) AS 'in_xref', p.Alias AS 'Alias'
  FROM $PXREF AS p
  ORDER BY PointSliceID ASC
";
$result = exec_sql($query);
$output = "
<tr>
  <th>PointSliceID</th>
  <th>PointName</th>
  <th>Alias</th>
  <th>Exists in $XREF</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $in_xref = $row['in_xref'];
  if($in_xref == "True") $class = 'in_xref';
  else $class = 'not_in_xref';
  $output .= "
  <tr>
    <td class='$class'>".$row['PointSliceID']."</td>
    <td class='$class'>".$row['PointName']."</td>
    <td class='$class' contenteditable='true'>".$row['Alias']."</td>
    <td class='$class'>".$row['in_xref']."</td>
  </tr>
  ";
}
echo $output;
?>
