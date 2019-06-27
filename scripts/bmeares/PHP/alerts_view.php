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


$query = 'SELECT * FROM CEVAC_ALL_ALERTS_HIST';
$head = "";
$head .= "<table style='width=100%'>";
$head .= "<tr>";
$head .= "<th>AlertID</th>";
$head .= "<th>AlertType</th>";
$head .= "<th>AlertMessage</th>";
$head .= "<th>Metric</th>";
$head .= "<th>BLDG</th>";
$head .= "<th>Acknowledged</th>";
$head .= "<th>BeginTime</th>";
$head .= "<th>EndTime</th>";
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
