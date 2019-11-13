<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
$TableName = clean($_GET['TableName']);
if(!isset($_GET['TableName'])){ die('missing params');}
echo table_exists($TableName);
?>
