<?php
include "../functions.php";
// var_dump($_POST);
$column = $_POST['column'];
$BuildingSName = $_POST['BuildingSName'];
$Metric = $_POST['Metric'];
$TableName = $_POST['TableName'];
$value = $_POST['value'];
$script = '/cevac/scripts/toggle_CEVAC_TABLES.sh';
$config = "";
$exec = "";

$default_zeroes = "
UPDATE CEVAC_TABLES
SET autoLASR = 0, autoCACHE = 0
WHERE BuildingSName = '$BuildingSName'
AND Metric = '$Metric'
";

if(!isset($_POST['TableName']) && (!isset($_POST['BuildingSName']) || !isset($_POST['Metric']))) die('missing params');
if(isset($_GET['t'])){
  $config = " -t $TableName";
} else{
  $config = " -b $BuildingSName -m $Metric";
}

foreach($_POST['attributes'] as $a){
  $exec .= $script.' -c '.$a.' -v 1'.$config.";\n";
}

exec_sql($default_zeroes);
echo "$exec";
echo `$exec`;

?>
