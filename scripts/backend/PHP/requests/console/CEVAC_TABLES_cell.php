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
if(!isset($_GET['Age'])) die('missing Age');
$Age = clean($_GET['Age']);

$query = "
  SELECT $column AS 'result' FROM CEVAC_TABLES
  WHERE BuildingSName = '$BuildingSName'
  AND Metric = '$Metric'
  AND Age = '$Age'
";
$result = sql_value($query);
echo "$result";

?>
