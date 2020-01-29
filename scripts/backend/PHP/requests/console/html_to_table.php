<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
if(!isset($_POST['fd'])) die('Missing fd');
if(!isset($_POST['headers'])) die('Missing headers');
if(!isset($_POST['tdata'])) die('Missing tdata');
// if(!isset($_POST['TableName'])) die('Missing TableName');
foreach($_POST['fd'] as $i){
  $i = clean($i);
  if($i['name'] == "BuildingSName") $BuildingSName = $i['value'];
  if($i['name'] == "Metric") $Metric = $i['value'];
  // if($i['name'] == "TableName") $TableName = $i['value'];
}
$TableName = $_POST['TableName'];
$TableNameBACKUP = $TableName."_HTML_BACKUP";
$headers = $_POST['headers'];
$TableNameINT = $TableName."_HTML_INT";
$query = "
IF OBJECT_ID('$TableNameINT') IS NOT NULL DROP TABLE $TableNameINT;
SELECT *
INTO $TableNameINT
FROM $TableName
WHERE 1 = 2";
exec_sql($query);
$iquery = "INSERT INTO $TableNameINT (";
$c = 0;
$identity_cols = [];
foreach($headers as $h){
  $idq = "SELECT COLUMNPROPERTY(OBJECT_ID('$TableName'),'".$h."','IsIdentity')";
  if(sql_value($idq) == 1){
    $identity_cols[] = $c;
    $c += 1;
    continue;
  }
  $iquery .= " $h,";
  $c += 1;
}
$iquery = substr($iquery, 0, -1).") VALUES (";

$query = "";
// for every row in the html table
for($i = 0; $i < sizeof($_POST['tdata']); $i++){
  $rquery = "";
  $row = $_POST['tdata'][$i];
  $c = 0;
  foreach($row as $v){
    // skip IDENITITY columns
    if(in_array($c, $identity_cols)){
      $c += 1;
      continue;
    }
    $v = html_entity_decode($v);
    if (strpos($v,"<br>") !== false) {
      $v = str_replace("<br>", "", $v);
    }
    $rquery .= " '".$v."',";
    $c += 1;
  }
  $rquery = $iquery.substr($rquery, 0, -1).");   \n";
  $query .= $rquery;
}
// echo "$query";
exec_sql($query);
$query = "
IF OBJECT_ID('$TableNameBACKUP') IS NOT NULL DROP TABLE $TableNameBACKUP;
SELECT * INTO $TableNameBACKUP FROM $TableName WHERE 1 = 1;
IF OBJECT_ID('$TableName') IS NOT NULL DROP TABLE $TableName;
EXEC sp_rename '$TableNameINT', '$TableName';
";
if(exec_sql($query)){
  echo "Successfully updated $TableName";
} else echo "Failed to update $TableName";
?>
