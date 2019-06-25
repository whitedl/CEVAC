<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
$query = urldecode($_GET['q']);
if(isset($_GET['debug'])) echo '<pre>';

$result = sqlsrv_query($db, $query);
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $json = json_encode($row);
  echo $json;
}


if(isset($_GET['debug'])) echo '</pre>';
sqlsrv_close($db);
?>
