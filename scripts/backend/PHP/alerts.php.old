<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
$query = '
  SELECT RTRIM(AlertType) AS AlertType, RTRIM(AlertMessage) AS AlertMessage,
  RTRIM(Metric) AS Metric, RTRIM(BuildingSName) AS BuildingSName, RTRIM(BuildingDName) AS BuildingDName, Acknowledged, EventID, ETDateTime, DetectionTimeET
  FROM CEVAC_ALL_ALERTS_EVENTS_HIST
  WHERE Acknowledged = 0
  ORDER BY EventID DESC;
';

if(isset($_GET['debug'])) echo '<pre>';

// $out = '[';
$array = array();


$result = sqlsrv_query($db, $query);
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $array[] = $row;
}

$out = json_encode($array);
// $out .= ']';
echo $out;


if(isset($_GET['debug'])) echo '</pre>';
sqlsrv_close($db);
?>
