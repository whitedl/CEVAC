<?php
include '/cevac/PHP/functions.php';
session_start();
enforce_login();
$command = 'sudo pkill websocketd';
$out = shell_exec($command);
echo $out."\nfinished";
?>
