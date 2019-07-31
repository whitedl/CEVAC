<?php
include "config.php";
global $db;

function stats($get){
  if(isset($get['BuildingSName']))
    $BuildingSName = clean($get['BuildingSName']);
  else $BuildingSName = "%";

  if(isset($get['Metric']))
    $Metric = clean($get['Metric']);
  else $Metric = "%";

  if(isset($get['OP']))
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

  sqlsrv_close($db);
  return $array;
}

?>
