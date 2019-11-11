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




function CEVAC_TABLES_value($TableName, $var){
  $query = "
  SELECT $var FROM CEVAC_TABLES
  WHERE TableName = '$TableName'
  ";
  return sql_value($query);
}
function CEVAC_CONFIG_value($var){
  $query = "
  SELECT VarValue FROM CEVAC_CONFIG
  WHERE VarName = '$var'
  ";
  return sql_value($query);
}

function validate_token($t){
  $fname = '/home/cevac/token.txt';
  $token = file_get_contents($fname);
  if($t == $token){
    return true;
  }
  return false;
}
function start_websocket($command){
  $command = "sudo -u cevac websocketd --port=8080 ".$command;
  // echo $command;
  // $descriptorspec = [
      // 0 => ['pipe', 'r'],
      // 1 => ['pipe', 'w'],
      // 2 => ['pipe', 'w']
  // ];
  // $proc = proc_open($command, $descriptorspec, $pipes);
  // $proc_details = proc_get_status($proc);
  // $pid = $proc_details['pid'];
  $pid = shell_exec($command);
  return $pid;
}

?>
