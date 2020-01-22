<?php
include "../../functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$column = clean($_POST['column']);
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);

if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');


$script = '/cevac/scripts/append_tables.sh';
$config = "";
$exec = "sudo -u cevac ".$script." -b $BuildingSName -m $Metric";
foreach($_POST['attributes'] as $a){
  $a = clean($a);
  if($a == "autoLASR"){
    $lasr_script = "/cevac/scripts/lasr_append.sh $BuildingSName $Metric HIST";
    $exec .= " && sudo -u cevac $lasr_script";
    $lasr_script = "/cevac/scripts/lasr_append.sh $BuildingSName $Metric LATEST";
    $exec .= " && sudo -u cevac $lasr_script";
  }
}
$exec .= "\n";
// echo "$exec";

echo `$exec`;


?>
