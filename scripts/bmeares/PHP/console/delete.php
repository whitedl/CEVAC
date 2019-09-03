<?php
include "../functions.php";
// var_dump($_POST);
$column = $_POST['column'];
$BuildingSName = $_POST['BuildingSName'];
$Metric = $_POST['Metric'];
$TableName = $_POST['TableName'];
$value = $_POST['value'];
$script = '/cevac/scripts/delete.sh';
$config = "";
$exec = $script." ".$BuildingSName." ".$Metric." -y";

if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');

echo "$exec";
echo `$exec`;

?>
