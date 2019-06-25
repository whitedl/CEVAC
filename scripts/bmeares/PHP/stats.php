<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
$bldg = $_GET['building'];
$bldg = clean($bldg);

$query = "SELECT RTRIM(building) AS building,
power_latest_sum,
temp_latest_avg,
co2_latest_avg,
report_link,
update_time 

FROM CEVAC_STATS
WHERE building = '$bldg'
";

$result = sqlsrv_query($db, $query);
$row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC);
$json = json_encode($row);

echo $json;

// while($row = sqlsrv_fetch_array($result)){
  // for($i = 0; $i < sizeof($row); $i++){
    // echo $row[$i]." ";
  // }
// }

sqlsrv_close($db);
?>
