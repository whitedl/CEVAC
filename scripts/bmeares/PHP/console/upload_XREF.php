<?php
include "../functions.php";

$BuildingSName = $_POST['BuildingSName'];
$Metric = $_POST['Metric'];
$unitOfMeasureID = $_POST['unitOfMeasureID'];
$key_words = $_POST['key_words'];

$script = '/cevac/python/CREATE_VIEW.sh';
$config = "";
$exec = "$script $BuildingSName $Metric PXREF";

echo "$exec";
// echo `$exec`;

?>
