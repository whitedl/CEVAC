<?php
include "functions.php";
global $db;

$stats = stats($_GET);
if(!isset($_GET['BuildingSName'])) die('Missing BuildingSName');

$BuildingSName = clean($_GET['BuildingSName']);



sqlsrv_close($db);
?>
