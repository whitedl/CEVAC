<?php
include "../../functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$column = clean($_POST['column']);
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);
$TableName = clean($_POST['TableName']);
$value = clean($_POST['value']);
$script = '/cevac/scripts/delete.sh';
$config = "";
$exec = $script." -b ".$BuildingSName." -m ".$Metric." -y";

if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');

// echo "$exec";
echo `$exec`;

?>
