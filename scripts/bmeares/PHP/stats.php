<?php
include "config.php";
global $db;

if(isset($_GET['BuildingSName']))
  $BuildingSName = clean($_GET['BuildingSName']);
else $BuildingSName = "%";

if(isset($_GET['Metric']))
  $Metric = clean($_GET['Metric']);
else $Metric = "%";

if(isset($_GET['OP']))
  $OP = clean($_GET['OP']);
else $OP = "*";

if($OP != "*") $extra_cols = ", DataName, last_ETDateTime, update_ETDateTime";
else $extra_cols = "";

$query = "
SELECT $OP".$extra_cols." FROM
CEVAC_ALL_LATEST_STATS
WHERE BuildingSName LIKE '$BuildingSName'
AND Metric LIKE '$Metric';
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
