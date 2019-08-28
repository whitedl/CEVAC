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
  $out = "";
  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
    $out .= "<option value='".$row['BuildingSName']."'>".$row['BuildingDName']."</option>\n";
  }
  return $out;
}

function metrics_html(){
  global $db;
  $query = "
    SELECT DISTINCT RTRIM(Metric) AS Metric, um.DisplayNameShort AS dn FROM CEVAC_METRIC AS cm
    INNER JOIN [130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure AS um ON um.UnitOfMeasureID = cm.unitOfMeasureID
    ORDER BY um.DisplayNameShort ASC
  ";
  $result = sqlsrv_query($db, $query);
  $out = "";
  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
    $out .= "<option value='".$row['Metric']."'>".$row['dn']."</option>\n";
  }
  return $out;
}

?>
