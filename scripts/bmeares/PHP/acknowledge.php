<?php
include "config.php";
global $db;

$method = $_SERVER['REQUEST_METHOD'];
if ('PUT' === $method) {
  parse_str(file_get_contents('php://input'), $_PUT);
  var_dump($_PUT); //$_PUT contains put fields 
}

echo $_PUT;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
// $query = '
  // SELECT RTRIM(AlertType) AS AlertType, RTRIM(AlertMessage) AS AlertMessage,
  // RTRIM(Metric) AS Metric, RTRIM(BuildingSName) AS BuildingSName, RTRIM(BuildingDName) AS BuildingDName, Acknowledged, EventID, ETDateTime, DetectionTimeET
  // FROM CEVAC_ALL_ALERTS_EVENTS_HIST
  // WHERE Acknowledged = 0
  // ORDER BY EventID DESC;
// ';

// if(isset($_GET['debug'])) echo '<pre>';

// // $out = '[';
// $array = array();


// $result = sqlsrv_query($db, $query);
// while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  // // $json = json_encode($row);
  // $array[] = $row;
  // // $out .= $json.',';
// }

// $out = json_encode($array);
// // $out .= ']';
// echo $out;


// if(isset($_GET['debug'])) echo '</pre>';
sqlsrv_close($db);
?>
