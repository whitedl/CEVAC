<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
// var_dump($_GET);
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$Age = clean($_GET['Age']);
$TableName = "CEVAC_$BuildingSName"."_$Metric"."_$Age";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric']) || !isset($_GET['Age'])) die('missing params');

$exists = table_exists($TableName);
if(!$exists){ die("$TableName does not exist. Click Rebuild PXREF to create the table."); }

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
  ORDER BY $IDName ASC
";
// die($query);
$result = exec_sql($query);

while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $in_xref = $row['in_xref'];
  if($in_xref == "1"){
    $class = 'in_xref';
    $check = '✔️';
  } else{
    $class = 'not_in_xref';
    $check = '❌';
  }

  $output .= "<tr>";
  foreach($row as &$c){
    $output .= "<td class='$class'>$c</td>";
  }
  $output .= "</tr>\n";
}
echo $output;






// include "../../functions.php";
// // var_dump($_POST);
// $BuildingSName = $_GET['BuildingSName'];
// $Metric = $_GET['Metric'];
// $PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
// $XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
// if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');

// $exists = table_exists($PXREF);
// if($exists == "DNE"){ die("$PXREF does not exist. Click Rebuild PXREF to create the table."); }

// $IDName = CEVAC_TABLES_value($PXREF, 'IDName');
// $AliasName = CEVAC_TABLES_value($PXREF, 'AliasName');


// $query = "
  // SELECT p.$IDName AS '$IDName', PointName AS 'PointName',
  // (CASE WHEN p.in_xref = 1 THEN 'True' ELSE 'False' END ) AS 'in_xref', p.$AliasName AS '$AliasName'
  // FROM $PXREF AS p
  // ORDER BY $IDName ASC
// ";
// // die($query);
// $result = exec_sql($query);
// $output = "
// <tr>
  // <th>$IDName</th>
  // <th>PointName</th>
  // <th>$AliasName</th>
  // <th>Exists in $XREF</th>
// </tr>
// ";

// while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  // $in_xref = $row['in_xref'];
  // if($in_xref == "True"){
    // $class = 'in_xref';
    // $check = '✔️';
  // }
  // else{
    // $class = 'not_in_xref';
    // $check = '❌';
  // }
  // $output .= "
  // <tr>
    // <td class='$class'>".$row[$IDName]."</td>
    // <td class='$class'>".$row['PointName']."</td>
    // <td class='$class' contenteditable='true'>".$row[$AliasName]."</td>
    // <td class='$class'>".$check."</td>
  // </tr>
  // ";
// }
// echo $output;
?>
