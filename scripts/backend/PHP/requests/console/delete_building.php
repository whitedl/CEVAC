<?php
include "../../functions.php";
// var_dump($_POST);
$BuildingSName = clean($_POST['BuildingSName']);
$script = '/cevac/scripts/delete.sh';

if(!isset($_POST['BuildingSName'])) die('missing params');

$query =  "
  SELECT DISTINCT BuildingSName, Metric FROM CEVAC_TABLES
  WHERE BuildingSName = '$BuildingSName';
";
$result = exec_sql($query);
$exec = "";
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $exec .= $script." -b \"".$row['BuildingSName']."\" -m \"".$row['Metric']."\" -y;\n";
}

$query = "DELETE FROM CEVAC_BUILDING_INFO WHERE BuildingSName = '$BuildingSName'";
exec_sql($query);

// echo "$exec";
echo `$exec`;

?>
