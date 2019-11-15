<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
$BuildingSName = clean($_GET['BuildingSName']);
$Metric = clean($_GET['Metric']);
if(!isset($_GET['BuildingSName']) || !isset($_GET['Metric'])) die('missing params');
$out = stats_html($BuildingSName, $Metric);
echo "$out";


?>
