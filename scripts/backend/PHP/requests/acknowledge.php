<?php
include "config.php";
global $db;


$method = $_SERVER['REQUEST_METHOD'];
if ('PATCH' === $method) {
  parse_str(file_get_contents('php://input'), $_PATCH);
  // var_dump($_PATCH); //$_PUT contains put fields 
}

// if(!isset($_REQUEST['EventID'])) $EventID = $_REQUEST['EventID'];
// else die('Missing EventID');
// if(!isset($_REQUEST['ACK'])) $ACK = $_REQUEST['ACK'];
// else die('Missing ACK');
//
$EventID = clean($_REQUEST['EventID']);
$ACK = clean($_REQUEST['ACK']);
$ACK = clean($ACK);
$EventID = clean($EventID);
if ($ACK != 0 && $ACK != 1) die('ACK must be 0 or 1.');

// $query = "
// UPDATE CEVAC_ALL_ALERTS_HIST_RAW
// SET Acknowledged = $ACK
// WHERE EventID = $EventID
// ";
$query = "EXEC CEVAC_ACKNOWLEDGE_EVENT @EventID = ".strval($EventID).", @ACK = ".strval($ACK);
// echo "$query";

$result = sqlsrv_query($db, $query);
// $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC);
// $json = json_encode($row);

// echo $json;
echo strval($EventID);

sqlsrv_close($db);
?>
