<?php
include "../../functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$DAY = "CEVAC_$BuildingSName"."_$Metric"."_DAY";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$exists = table_exists($DAY);
if($exists == "DNE"){ die("$DAY does not exist."); }

$IDName = CEVAC_TABLES_value($DAY, 'IDName');
$AliasName = CEVAC_TABLES_value($DAY, 'AliasName');
$DateTimeName = CEVAC_TABLES_value($DAY, 'DateTimeName');
$DataName = CEVAC_TABLES_value($DAY, 'DataName');

$query = "
  SELECT $AliasName, $DateTimeName, $DataName
  FROM $DAY
  ORDER BY $DateTimeName DESC
";
// die($query);
$result = exec_sql($query);
$output = "
<tr>
  <th>$AliasName</th>
  <th>$DateTimeName</th>
  <th>$DataName</th>
</tr>
";

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $output .= "
  <tr>
    <td class='$class'>".$row[$AliasName]."</td>
    <td class='$class'>".$row[$DateTimeName]."</td>
    <td class='$class'>".$row[$DataName]."</td>
  </tr>
  ";
}
echo $output;
?>
