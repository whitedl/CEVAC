<?php
include '/cevac/PHP/functions.php';
session_start();
enforce_login();
if(!isset($_GET['BuildingSName'])) die('Missing BuildingSName');
echo metrics_html(clean($_GET['BuildingSName']), clean($_GET['filter']));

?>
