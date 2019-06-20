<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
// $bldg = $vars['building'];
// $type = $vars['type'];
// $metric = $vars['metric'];
// $begin = $vars['begin'];
// $end = $vars['end'];


$query = 'SELECT SUM(ActualValue) AS SUM FROM CEVAC_WATT_POWER_LATEST';

$result = sqlsrv_query($db, $query);
while($val = sqlsrv_fetch_array($result)){
  echo $val[0];
}

// echo "<p>Hello, World!</p>";
?>
