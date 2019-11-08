<?php
include '../../functions.php';
$token = $_POST['token'];
// if(!validate_token($token)) die('invalid token');
$pid = start_websocket('/cevac/scripts/test.sh');
echo $pid;
echo "\nrunning";
?>
