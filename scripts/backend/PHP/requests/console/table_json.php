<?php
include "../../functions.php";
// var_dump($_POST);
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$Age = clean($_GET['Age']);
$TableName = "CEVAC_$BuildingSName"."_$Metric"."_$Age";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric']) || !isset($_GET['Age'])) die('missing params');

$exists = table_exists($TableName);
if($exists == "DNE"){ die("$TableName does not exist. Click Rebuild PXREF to create the table."); }

$IDName = CEVAC_TABLES_value($TableName, 'IDName');
$AliasName = CEVAC_TABLES_value($TableName, 'AliasName');
$DateTimeName = CEVAC_TABLES_value($TableName, 'DateTimeName');
$DataName = CEVAC_TABLES_value($TableName, 'DataName');

// $result = get_columns($TableName);
$j_array = [];
// while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  // $j_array[] = $row;
// }
// $output .= "</tr>";
// $cols = substr($cols, 0, strlen($cols) - 2);

$query = "
  SELECT *
  FROM $TableName
  ORDER BY $DateTimeName DESC
";
// die($query);
$result = exec_sql($query);

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $j_array[] = $row;
}
echo json_encode($j_array);
?>
