<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
$column = clean($_POST['column']);
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);
if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');
$reset_csv = false;
if(isset($_POST['reset_csv_check'])){
  if(clean($_POST['reset_csv_check']) == "on")
    $reset_csv = true;
}
if($reset_csv)
  echo "reset!\n";
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
  if($reset_csv) $exec .= "rm /srv/csv/$TableName.csv$continue";
  $exec .= $script." ".$BuildingSName." ".$Metric." ".$Age.$config.$continue;
}
$exec = substr($exec, 0, (strlen($config.$continue) * -1));
$exec.= " norun reset\n";

echo "$exec";
// echo `$exec`;

?>
