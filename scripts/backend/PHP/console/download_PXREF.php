<?php
include "../functions.php";
// var_dump($_POST);
$BuildingSName = $_GET['BuildingSName'];
$Metric = $_GET['Metric'];
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');
$script = "sudo -u cevac /cevac/scripts/table_to_csv_append.sh";
$config = "\"$PXREF\" \"reset\"";
// Create CSV file
$output = `$script $config`;

echo "csv/$PXREF.csv";
?>
