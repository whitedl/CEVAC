<?php
include "config.php";
global $db;

if(isset($_GET['beginET']))
  $beginET = "'".clean($_GET['beginET'],[':'])."'";
else $beginET = "0";

$query = "
DECLARE @begin DATETIME;
SET @begin = CAST(".$beginET." AS DATETIME);
SELECT P_UTCDateTime, ETDateTime, P_Total_Usage, Total_Usage FROM
CEVAC_WATT_POWER_SUMS_COMPARE_HIST
WHERE P_ETDateTime > @begin
ORDER BY P_ETDateTime DESC;
";


$array = array();
$result = sqlsrv_query($db, $query);
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $array[] = $row;
}

$json = json_encode($array);
echo $json;

sqlsrv_close($db);
?>
