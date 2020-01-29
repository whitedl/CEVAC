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
if(!$exists){ die("$TableName does not exist. Click Rebuild PXREF to create the table."); }

$IDName = CEVAC_TABLES_value($TableName, 'IDName');
$AliasName = CEVAC_TABLES_value($TableName, 'AliasName');
$DateTimeName = CEVAC_TABLES_value($TableName, 'DateTimeName');
$DataName = CEVAC_TABLES_value($TableName, 'DataName');

$j_array = [];
$keys_query = "
  SELECT TOP 1 *
  FROM CEVAC_TABLES
  WHERE TableName = '$TableName'
";
$result = exec_sql($keys_query);

$keys = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC);
$j_array['keys'] = $keys;
$query = "
  SELECT *
  FROM $TableName
  ORDER BY $DataName DESC
";
$result = exec_sql($query);
$data_array = [];
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $data_array[] = $row;
}
$j_array['data'] = $data_array;

echo json_encode($j_array);
?>
