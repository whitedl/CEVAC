<?php
  include "functions.php";
?>
<!DOCTYPE html>
<html>
	<head>
    <meta charset="utf-8" />
    <title>CEVAC Database Management</title>
    <link rel="stylesheet" type="text/css" href="css/har.css">
    <link rel="stylesheet" type="text/css" href="css/slider.css">
    <script src="console/JS/console.js"></script>
    <script src="console/JS/format.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	</head>
	<body>
    <a onclick="show_hide('advanced_div')" href="#">Advanced options</a><br><br>
    <select id="actions_select" onchange="get_Metrics_html()">
      <option value="existing">Manage existing</option>
      <option value="new">New</option>
    </select>
    <form method="post" id="toggle">
      <?php echo buildings_html(); ?>
      <select name="Metric" id="metrics" style="display: none"></select><br>

      <div id="autoCACHE_div" style="display:none">
        <h4>autoCACHE</h4>
        <label for="autoCACHE" id="autoCACHE_label" class="switch">
          <input type="checkbox" name="attributes[]" value="autoCACHE" id='autoCACHE' onclick="toggle()">
          <span class="slider round"></span>
        </label>
      </div>
      <div id="autoLASR_div" style="display:none">
        <h4>autoLASR</h4>
        <label for="autoLASR" id="autoLASR_label" class="switch">
          <input type="checkbox" name="attributes[]" value="autoCACHE" id='autoLASR' onclick="toggle()">
          <span class="slider round"></span>
        </label>
      </div>

      <div id='advanced_div' style="display: none">
        <p>Lorem ipsum dolor</p>
      </div>
    </form>
    <br>
    <div id="buttons_div" style="display:none">
      <button name="bootstrap_button" id="bootstrap_button" onclick="bootstrap()">Bootstrap</button>
      <button name="delete_button" id="delete_button" onclick="del()">Delete</button>
    </div>
    <pre id="output"></pre>
	</body>
</html>
