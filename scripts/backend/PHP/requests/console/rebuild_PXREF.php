<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();

$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);
$unitOfMeasureID = clean($_POST['unitOfMeasureID']);
$key_words = clean($_POST['key_words']);

$script = '/cevac/scripts/CREATE_VIEW.sh';
$config = "";
$exec = "$script $BuildingSName $Metric PXREF";

echo "$exec\n";
echo `$exec`;

?>
