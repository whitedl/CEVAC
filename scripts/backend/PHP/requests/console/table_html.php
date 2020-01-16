<?php
include "../../functions.php";
// var_dump($_GET);
session_start();
enforce_login();
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$Age = clean($_GET['Age']);
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['TableName'])){
  if(!isset($_GET['BuildingSName']) ||
    !isset($_GET['Metric']) ||
    !isset($_GET['Age'])){
      die('missing params');
  }
  $TableName = "CEVAC_$BuildingSName"."_$Metric"."_$Age";
} else {
  $TableName = clean($_GET['TableName'],$exclude_array=['_']);
}
$editable = false;
if(isset($_GET['editable']))
  if($_GET['editable'] == 'true')
    $editable = true;

$exists = table_exists($TableName);
if($exists == "DNE"){ die("$TableName does not exist. Click Rebuild PXREF to create the table."); }
$output = table_html($TableName,$editable=$editable);

echo $output;
?>
