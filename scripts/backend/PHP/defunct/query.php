<html>
<head>
<link rel="stylesheet" type="text/css" href="iframe.css">

</head>
<?php
include "../config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
$query = urldecode($_GET['q']);
if(isset($_GET['debug'])) echo '<pre>';

$result = sqlsrv_query($db, $query);
echo "<table>\n";
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  echo "\t<tr>\n";
  foreach($row as $row_value){
      echo "\t\t<td>$row_value</td>\n";
  }
  echo "\t</tr>\n";
  // $json = json_encode($row);
  // echo $json;
}
echo "</table>\n";


if(isset($_GET['debug'])) echo '</pre>';
sqlsrv_close($db);
?>

</html>
