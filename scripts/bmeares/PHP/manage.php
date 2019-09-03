<?php
  include "functions.php";
?>
<!DOCTYPE html>
<html>
	<head>
    <meta charset="utf-8" />
    <title>CEVAC Database Management</title>
    <link rel="stylesheet" type="text/css" href="har.css">
    <script src="console/JS/console.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	</head>
	<body>
    <form method="post" id="toggle">
      <?php echo buildings_html(); ?>
      <option name="Metric" id="metrics" style="display: none"></option><br>
      <input style="display: none" type="checkbox" name="attributes[]" value="autoCACHE" id='autoCACHE' onclick="toggle()">
      <label for="autoCACHE" id="autoCACHE_label" style="display: none">autoCACHE</label>
      <input style="display: none" type="checkbox" name="attributes[]" value="autoLASR" id='autoLASR' onclick="toggle()">
      <label for="autoLASR" id="autoLASR_label" style="display: none">autoLASR</label>
    </form>
    <br>
    <div id="buttons_div" style="display:none">
      <button name="bootstrap_button" id="bootstrap_button" onclick="bootstrap()">Bootstrap</button>
      <button name="delete_button" id="delete_button" onclick="del()">Delete</button>
    </div>
    <pre id="output"></pre>
	</body>
</html>
