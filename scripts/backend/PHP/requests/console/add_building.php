<?php
include "/cevac/PHP/functions.php";
$new_BuildingSName = clean($_POST['new_BuildingSName']);
$new_BuildingDName = clean($_POST['new_BuildingDName'],['\s']);
$new_BuildingKey = clean($_POST['new_BuildingKey']);

$script = 'sudo -u cevac /cevac/scripts/add_building.sh';
$config = "-b $BuildingSName -d $BuildingDName -k $BuildingKey";
$exec = $script." -b \"$new_BuildingSName\" -d \"$new_BuildingDName\" -k \"$new_BuildingKey\"";

if(!isset($_POST['new_BuildingSName']) || 
  !isset($_POST['new_BuildingDName']) ||
  !isset($_POST['new_BuildingKey'])
) die('missing params');

echo "$exec";
echo `$exec`;

?>
