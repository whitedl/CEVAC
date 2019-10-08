<?php
include "../functions.php";
$new_BuildingSName = $_POST['new_BuildingSName'];
$new_BuildingDName = $_POST['new_BuildingDName'];
$new_BuildingKey = $_POST['new_BuildingKey'];

$script = '/cevac/scripts/add_building.sh';
$config = "-b $BuildingSName -d $BuildingDName -k $BuildingKey";
$exec = $script." -b \"$new_BuildingSName\" -d \"$new_BuildingDName\" -k \"$new_BuildingKey\"";

if(!isset($_POST['new_BuildingSName']) || 
  !isset($_POST['new_BuildingDName']) ||
  !isset($_POST['new_BuildingKey'])
) die('missing params');

echo "$exec";
echo `$exec`;

?>
