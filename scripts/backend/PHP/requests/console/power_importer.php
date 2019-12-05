<?php
include "../../functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$column = clean($_POST['column']);
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);


$script = 'python3 /cevac/cron/power/all_powermeters_importer.py';
$exec = "sudo -u cevac ".$script." 2>&1";
// echo "$exec";

echo `$exec`;


?>
