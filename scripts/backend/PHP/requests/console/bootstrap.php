<?php
include "../../functions.php";
// var_dump($_POST);
$column = clean($_POST['column']);
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);
$TableName = clean($_POST['TableName']);
$value = clean($_POST['value']);
$script = '/cevac/scripts/bootstrap.sh';
$config = "";
$exec = "sudo -u cevac ".$script." -b $BuildingSName -m $Metric -y";

if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');
foreach($_POST['attributes'] as $a){
  $a = clean($a);
  if($a == "autoCACHE") $exec .= " -c";
  if($a == "autoLASR") $exec .= " -l";
}
$exec .= "\n";
// echo "$exec";
echo `$exec`;
?>
