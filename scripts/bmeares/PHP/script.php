<html>
<body>
<pre>
<?php

$script = urldecode($_GET['s']);

if(isset($_GET['s'])){
  echo shell_exec('/home/bmeares/scripts/'.$script);
}


?>
</pre>
</body>
</html>
