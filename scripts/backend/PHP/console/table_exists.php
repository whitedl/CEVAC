<?php
include "../functions.php";
$TableName = $_GET['TableName'];
if(!isset($_GET['TableName'])){ die('missing params');}
echo table_exists($TableName);
?>
