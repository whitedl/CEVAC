<?php
include "config.php";
global $db;


$query = '
SELECT UnitOfMeasureID, UnitOfMeasureName, MeasureType, DisplayNameShort
FROM [130.127.238.129].JCIHistorianDB.dbo.tblUnitOfMeasure
';
$head = "";
$head .= "<table style='width=100%'>";
$head .= "<tr>";
$head .= "<th>UnitOfMeasureID</th>";
$head .= "<th>UnitOfMeasureName</th>";
$head .= "<th>MeasureType</th>";
$head .= "<th>DisplayNameShort</th>";
$head .= "</tr>";

$body = "";

$result = sqlsrv_query($db, $query);

// for($i = 0; $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC) && $i < 20; $i++ ){
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $body .= "<tr>";
  foreach($row as &$val) $body .= "<td>".$val."</td>";
  for($i = 0; $i < sizeof($row); $i++) $body .= "<td>".$row[$i]."</td>";
  $body .= "</tr>";
}
$body .= "</table>";

echo $head.$body;

sqlsrv_close($db);
?>
