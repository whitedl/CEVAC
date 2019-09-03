<?php
include '../functions.php';
if(!isset($_GET['BuildingSName'])) die('Missing BuildingSName');
echo metrics_html($_GET['BuildingSName']);

?>
