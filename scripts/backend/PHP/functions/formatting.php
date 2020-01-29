<?php
include_once "../functions.php";
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
function stats_html($BuildingSName, $Metric){
  $query = "
  SELECT TOP 1 DataName, AVG, SUM, MIN, MAX, last_ETDateTime, update_ETDateTime
  FROM CEVAC_ALL_LATEST_STATS
  WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric';
  ";
  $LATEST = "CEVAC_$BuildingSName"."_$Metric"."_LATEST";
  $result = exec_sql($query);
  // $out = "<table>\n  <tr>";
  $out = "<th>Statistic</th>\n<th>Value</th>\n";
  $out .= "  </tr>\n";
  $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC);
  if(count($row) == 0) return "No statistics found for $LATEST";
  foreach ($row as $c => $val){
    $out .= "  <tr>";
    $out .= "    <td>$c</td>";
    $out .= "    <td>$val</td>";
    $out .= "  </tr>";
  }
  // $out .= "\n</table>";
  return $out;
}
function table_html($TableName,$editable=false, $order_by=""){
  $IDName = CEVAC_TABLES_value($TableName, 'IDName');
  $AliasName = CEVAC_TABLES_value($TableName, 'AliasName');
  $DateTimeName = CEVAC_TABLES_value($TableName, 'DateTimeName');
  $DataName = CEVAC_TABLES_value($TableName, 'DataName');

  $result = get_columns($TableName);
  $cols = "";
  $output = "<tr>";
  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_NUMERIC)){
    $cols .= $row[0].", ";
    $output .= "<th>".$row[0]."</th>\n";
  }
  $output .= "</tr>";
  $cols = substr($cols, 0, strlen($cols) - 2);

  $query = "
    SELECT $cols
    FROM $TableName
  ";
  if($DateTimeName != ''){
    $order_by = "$DateTimeName DESC";
    // $query .= "\nORDER BY $DateTimeName DESC";
  }
  if ($order_by != "") $query .= "ORDER BY $order_by";
  // die($query);
  $result = exec_sql($query);

  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_NUMERIC)){
    $output .= "<tr>";
    foreach($row as &$c){
      $output .= "<td";
      if($editable) $output .= " contenteditable='true'";
      $output .= ">".htmlspecialchars($c)."</td>";
    }
    $output .= "</tr>\n";
  }
  return $output;
}
function gen_TableName($BuildingSName, $Metric, $Age){
  $TableName = "CEVAC_".$BuildingSName."_".$Metric;
  if($Age != "") $TableName .= "_".$Age;
  return $TableName;
}
?>
