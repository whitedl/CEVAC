<?php
$command = 'sudo pkill websocketd';
$out = shell_exec($command);
echo $out."\nfinished";
?>
