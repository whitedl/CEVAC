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
$EventID = $_REQUEST['EventID'];
$RES = $_REQUEST['RES'];
$RES = clean($RES);
$EventID = clean($EventID);
if ($RES != 0 && $RES != 1) die('RES must be 0 or 1.');

// $query = "
// UPDATE CEVAC_ALL_ALERTS_HIST_RAW
// SET Acknowledged = $ACK
// WHERE EventID = $EventID
// ";
$query = "EXEC CEVAC_RESOLVE_EVENT @EventID = ".strval($EventID).", @RES = ".strval($RES);
// echo "$query";

$result = sqlsrv_query($db, $query);
// $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC);
// $json = json_encode($row);

// echo $json;
echo strval($EventID);

sqlsrv_close($db);
?>
