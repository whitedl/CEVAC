<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();
$BuildingSName = clean($_POST['BuildingSName']);
$Metric = clean($_POST['Metric']);
$XREF = "CEVAC_$BuildingSName"."_$Metric"."_XREF";
$pred_filename = $XREF.".CSV";
if(!isset($_POST['BuildingSName']) || !isset($_POST['Metric'])) die('missing params');

$tmp_name = $_FILES['file']['tmp_name'];
$name = strtoupper(clean($_FILES['file']['name'],['_','.']));
$dest_name = "/cevac/cache/".$name;
if($name != $pred_filename) die("Filename does not match BuildingSName and Metric. Check the drop down menus.\n");

if(copy($tmp_name, $dest_name)){
  echo "success\n";
} else echo "failure\n";
// $script = 'python3 /cevac/CEVAC/scripts/lingxiao/PointSliceID_Xref/csv_process.py';
// $exec = "sudo -u cevac $script -f $dest_name -b \"$BuildingSName\" -m \"$Metric\" -a \"XREF\"";
$exec = "sudo -u cevac python3 /cevac/python/csv_process.py $dest_name 2>&1";

echo "$exec\n";
echo passthru($exec);

$query = "
DELETE FROM CEVAC_TABLES WHERE TableName = '$XREF';
INSERT INTO CEVAC_TABLES(BuildingSName, Metric, Age, TableName, DateTimeName, AliasName, DataName, isCustom, customLASR, autoCACHE, autoLASR)
VALUES (
  '$BuildingSName',
  '$Metric',
  'XREF',
  '$XREF',
  'PointSliceID',
  'Alias',
  'PointSliceID',
  1,
  0,
  0,
  0
);
";
exec_sql($query);

?>
