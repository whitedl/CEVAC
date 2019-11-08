<?php
include "../functions.php";
// var_dump($_POST);
$column = $_POST['column'];
$BuildingSName = $_POST['BuildingSName'];
$Metric = $_POST['Metric'];
$TableName = $_POST['TableName'];
$value = $_POST['value'];
$script = '/cevac/scripts/bootstrap.sh';
$config = "";
$exec = "sudo -u cevac ".$script." -b $BuildingSName -m $Metric -y";

if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');
foreach($_POST['attributes'] as $a){
  if($a == "autoCACHE") $exec .= " -c";
  if($a == "autoLASR") $exec .= " -l";
}
$exec .= "\n";
// echo "$exec";
echo `$exec`;
?>
