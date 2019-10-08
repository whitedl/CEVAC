<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$exists = table_exists($PXREF);
if($exists == "DNE"){ die("$PXREF does not exist. Click Rebuild PXREF to create the table."); }

$IDName = CEVAC_TABLES_value($PXREF, 'IDName');
$AliasName = CEVAC_TABLES_value($PXREF, 'AliasName');


$query = "
  SELECT p.$IDName AS '$IDName', PointName AS 'PointName',
  (CASE WHEN p.in_xref = 1 THEN 'True' ELSE 'False' END ) AS 'in_xref', p.$AliasName AS '$AliasName'
  FROM $PXREF AS p
  ORDER BY $IDName ASC
";
// die($query);
$result = exec_sql($query);
$output = "
<tr>
  <th>$IDName</th>
  <th>PointName</th>
  <th>$AliasName</th>
  <th>Exists in $XREF</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $in_xref = $row['in_xref'];
  if($in_xref == "True"){
    $class = 'in_xref';
    $check = '✔️';
  }
  else{
    $class = 'not_in_xref';
    $check = '❌';
  }
  $output .= "
  <tr>
    <td class='$class'>".$row[$IDName]."</td>
    <td class='$class'>".$row['PointName']."</td>
    <td class='$class' contenteditable='true'>".$row[$AliasName]."</td>
    <td class='$class'>".$check."</td>
  </tr>
  ";
}
echo $output;
?>
