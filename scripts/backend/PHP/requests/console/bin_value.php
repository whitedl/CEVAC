<?php
include '../../functions.php';
session_start();
enforce_login();
if(!isset($_GET['column'])) die('missing column');
$column = clean($_GET['column']);
if(!isset($_GET['BuildingSName'])) die('missing BuildingSName');
$BuildingSName = clean($_GET['BuildingSName']);
if(!isset($_GET['Metric'])) die('missing Metric');
$Metric = clean($_GET['Metric']);

$query = "
IF EXISTS(
  SELECT $column FROM CEVAC_TABLES
  WHERE $column = 1
  AND BuildingSName = '$BuildingSName'
  AND Metric = '$Metric'
) SELECT '1' AS e
ELSE SELECT '0' AS e
";
$result = exec_sql($query);
$row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC);
echo $row['e'];

?>
