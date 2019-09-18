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

function buildings_html(){
  global $db;
  $query = "
    SELECT DISTINCT RTRIM(BuildingSName) AS BuildingSName, RTRIM(BuildingDName) AS BuildingDName
    FROM CEVAC_BUILDING_INFO
    ORDER BY BuildingDName ASC";
  $result = sqlsrv_query($db, $query);
  $out = "<select id='buildings' name='BuildingSName' onchange='get_Metrics_html()'>\n";
  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
    $out .= "<option value='".$row['BuildingSName']."'>".$row['BuildingDName']."</option>\n";
  }
  $out .= "\n</select>";
  return $out;
}

function metrics_html($BuildingSName, $filter){
  global $db;
  if($filter == "existing"){
    $query = "
    SELECT DISTINCT RTRIM(ct.Metric) AS Metric, ISNULL(um.DisplayNameShort, 'No units') AS dn
    FROM CEVAC_TABLES AS ct
    LEFT OUTER JOIN CEVAC_METRIC AS cm ON cm.Metric = ct.Metric
    LEFT OUTER JOIN tblUnitOfMeasure AS um ON um.UnitOfMeasureID = cm.unitOfMeasureID
    WHERE BuildingSName = '$BuildingSName'
    AND Age = 'HIST'
    ";
  } else {
    $query = "
    SELECT DISTINCT RTRIM(cm.Metric) AS Metric, ISNULL(um.DisplayNameShort, 'No units') AS dn
    FROM CEVAC_METRIC AS cm
    LEFT OUTER JOIN tblUnitOfMeasure AS um ON um.UnitOfMeasureID = cm.unitOfMeasureID
    ";
  }
  
  $result = sqlsrv_query($db, $query);
  $out = "<select id='metrics' name='Metric' onchange='get_attributes_html()'>\n";
  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
    $out .= "<option value='".$row['Metric']."'>".$row['Metric']." (".$row['dn'].")"."</option>\n";
  }
  $out .= "\n</select>";
  return $out;
}

function exec_sql($query){
  global $db;
  $result = sqlsrv_query($db, $query);
  if($result === false) die(print_r(sqlsrv_errors(), true));
  return $result;
}
function sql_value($query){
  $result = exec_sql($query);
  $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_NUMERIC);
  if($row === false) die(print_r(sqlsrv_errors(), true));
  return $row[0];
}
function CEVAC_CONFIG_value($var){
  $query = "
  SELECT VarValue FROM CEVAC_CONFIG
  WHERE VarName = '$var'
  ";
  return sql_value($query);
}
?>
