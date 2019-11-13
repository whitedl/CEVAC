<?php
include "/cevac/PHP/functions.php";
session_start();
enforce_login();

$tmp_name = $_FILES['file']['tmp_name'];
$name = strtoupper($_FILES['file']['name']);
$dest_name = "/cevac/cache/".$name;
if(copy($tmp_name, $dest_name)){
  echo "success\n";
} else echo "failure\n";
$script = '/cevac/scripts/upload_XREF.sh';
$exec = "sudo -u cevac $script $dest_name";

echo "$exec\n";
echo passthru($exec);

?>
