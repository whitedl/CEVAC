<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
$query = '
  SELECT AlertID, RTRIM(AlertType) AS AlertType, RTRIM(AlertMessage) AS AlertMessage,
  RTRIM(Metric) AS Metric, RTRIM(BLDG) AS BLDG, Acknowledged, BeginTime, EndTime
  FROM CEVAC_ALL_ALERTS_HIST
  WHERE Acknowledged = 0
  ORDER BY AlertID DESC;
';

if(isset($_GET['debug'])) echo '<pre>';

// $out = '[';
$array = array();


$result = sqlsrv_query($db, $query);
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  // $json = json_encode($row);
  $array[] = $row;
  // $out .= $json.',';
}

$out = json_encode($array);
// $out .= ']';
echo $out;


if(isset($_GET['debug'])) echo '</pre>';
sqlsrv_close($db);
?>
