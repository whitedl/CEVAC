<?php
include '../../functions.php';
if(!isset($_GET['BuildingSName'])) die('Missing BuildingSName');
echo metrics_html(clean($_GET['BuildingSName']), clean($_GET['filter']));

?>
