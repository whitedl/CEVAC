<?php
  include "functions.php";
?>
<!DOCTYPE html>
<html>
	<head>
    <meta charset="utf-8" />
		<title>CEVAC Database Management</title>
    <script src="console/JS/console.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	</head>
	<body>
    <form method="post" id="toggle">
      <?php echo buildings_html(); ?>
      <?php echo metrics_html(); ?>
      <input type="checkbox" name="attributes" value="autoCACHE">autoCACHE<br>
      <input type="checkbox" name="attributes" value="autoLASR">autoLASR<br>
    </form>

    <br>
    <button onclick="toggle()">Toggle</button>

    <pre id="output">Test</pre>
	</body>
</html>
