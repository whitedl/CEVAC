<?php
include "../functions.php";

$tmp_name = $_FILES['file']['tmp_name'];
$name = strtoupper($_FILES['file']['name']);
$dest_name = "/cevac/cache/".$name;
if(copy($tmp_name, $dest_name)){
  echo "success\n";
} else echo "failure\n";
// $script = '/cevac/scripts/upload_XREF.sh';
$script = 'python3 /home/cevac/temp/test.py';
$exec = "sudo $script $dest_name";

echo "$exec\n";
echo passthru($exec);

?>
