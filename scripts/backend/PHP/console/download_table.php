<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$Age = $_GET['Age'];
$TableName = "CEVAC_$BuildingSName"."_$Metric"."_$Age";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric']) ||
!isset($_GET['Age'])) die('missing params');
$script = "sudo -u cevac /cevac/scripts/table_to_csv_append.sh";
$config = "\"$TableName\" \"reset\"";
// Create CSV file
$output = `$script $config`;

echo "csv/$TableName.csv";
?>
