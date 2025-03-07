<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
// var_dump($_POST);
$column = clean($_POST['column']);
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);
if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');
$rebuild_csv = false;
if(isset($_POST['rebuild_csv_check'])){
  if(clean($_POST['rebuild_csv_check']) == "on")
    $rebuild_csv = true;
}
$script = 'sudo -u cevac /cevac/scripts/lasr_append.sh';
$exec = "";
$query = "
SELECT Age
FROM CEVAC_TABLES
WHERE BuildingSName = '$BuildingSName' AND Metric = '$Metric'
AND autoLASR = 1
";
$result = exec_sql($query);

$continue = " && \\\n";
$config = " norun reset";
while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  $Age = $row['Age'];
  $TableName = gen_TableName($BuildingSName, $Metric, $Age); 
  if($rebuild_csv) $exec .= "rm /srv/csv/$TableName.csv$continue";
  $exec .= $script." ".$BuildingSName." ".$Metric." ".$Age.$config.$continue;
}
$exec = substr($exec, 0, (strlen($config.$continue) * -1));
$exec .= " norun reset\n";

echo "$exec";
echo `$exec`;

?>
