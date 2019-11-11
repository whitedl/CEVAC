<?php
include "../../functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
$PXREF = "CEVAC_$BuildingSName"."_$Metric"."_PXREF";
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');
$script = "sudo -u cevac /cevac/scripts/table_to_csv_append.sh";
$config = "\"$XREF\" \"reset\"";
// Create CSV file
$output = `$script $config`;
// echo "$output";

echo "csv/$XREF.csv";
?>
