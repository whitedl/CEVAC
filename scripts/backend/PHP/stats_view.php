<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
// $bldg = $vars['building'];
// $type = $vars['type'];
// $metric = $vars['metric'];
// $begin = $vars['begin'];
// $end = $vars['end'];
// $url = $vars['url'];


$query = 'SELECT * FROM CEVAC_STATS';
$head = "";
$head .= "<table style='width=100%'>";
$head .= "<tr>";
$head .= "<th>Building</th>";
$head .= "<th>Power Latest Sum</th>";
$head .= "<th>Temperature Latest Average</th>";
$head .= "<th>CO2 Latest Average</th>";
$head .= "<th>Report URL</th>";
$head .= "<th>Update Time</th>";
$head .= "</tr>";

$body = "";

$result = sqlsrv_query($db, $query);

// for($i = 0; $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC) && $i < 20; $i++ ){
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $body .= "<tr>";
  foreach($row as &$val) $body .= "<td>".$val."</td>";
  for($i = 0; $i < sizeof($row); $i++) $body .= "<td>".$row[$i]."</td>";
  $body .= "</tr>";
}
$body .= "</table>";

echo $head.$body;

sqlsrv_close($db);
?>
