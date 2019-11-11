<?php
include "../../functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$Age = clean($_GET['Age']);
$LATEST = "CEVAC_$BuildingSName"."_$Metric"."_LATEST";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

$exists = table_exists($LATEST);
if($exists == "DNE"){ die("$LATEST does not exist. Click Rebuild PXREF to create the table."); }

$IDName = CEVAC_TABLES_value($LATEST, 'IDName');
$AliasName = CEVAC_TABLES_value($LATEST, 'AliasName');
$DateTimeName = CEVAC_TABLES_value($LATEST, 'DateTimeName');
$DataName = CEVAC_TABLES_value($LATEST, 'DataName');

$query = "
  SELECT $AliasName, $DateTimeName, $DataName
  FROM $LATEST
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
