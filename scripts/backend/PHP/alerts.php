<?php
include "config.php";
global $db;

$where = " WHERE ";
foreach($_GET as $g){
  $key = array_search($g, $_GET);
  $where .= " $key = '$g' AND";
}
if(count($_GET) > 0) $where = substr($where, 0, -3);
else $where = "";

$query = "
SELECT
  RTRIM(AlertType) AS AlertType,
  RTRIM(AlertMessage) AS AlertMessage,
  RTRIM(Metric) AS Metric,
  RTRIM(BuildingSName) AS BuildingSName,
  RTRIM(BuildingDName) AS BuildingDName,
  Acknowledged,
  EventID,
  ETDateTime,
  DetectionTimeET,
  Resolved
FROM CEVAC_ALL_ALERTS_EVENTS_HIST
$where
";

// echo $query;
$array = array();
$result = sqlsrv_query($db, $query);
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $array[] = $row;
}

$json = json_encode($array);
echo $json;
sqlsrv_close($db);
?>
