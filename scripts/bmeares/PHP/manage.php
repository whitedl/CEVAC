<?php
  include "functions.php";
?>
<!DOCTYPE html>
<html>
	<head>
    <meta charset="utf-8" />
    <title>CEVAC Database Management</title>
    <link rel="stylesheet" type="text/css" href="css/har.css">
    <link rel="stylesheet" type="text/css" href="css/custom.css">
    <link rel="stylesheet" type="text/css" href="css/slider.css">
    <link rel="stylesheet" type="text/css" href="css/radio.css">
    <script src="console/JS/console.js"></script>
    <script src="console/JS/format.js"></script>
    <script src="console/JS/pull.js"></script>
    <script src="console/JS/push.js"></script>
    <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js"></script>
	</head>
	<body onload="get_Metrics_html()">
    <a onclick="show_hide_class('advanced');" href="#">Advanced options</a><br><br>
    <div id="body_left">
      <form method="post" id="toggle">
				<label class="container">Existing
					<input type="radio" checked="checked" name="actions_select" value="existing" onchange="get_Metrics_html()">
					<span class="checkmark"></span>
				</label>
				<label class="container">New
					<input type="radio" name="actions_select" value="new" onchange="get_Metrics_html()">
					<span class="checkmark"></span>
				</label>
       <?php echo buildings_html(); ?>
        <select name="Metric" id="metrics" style="display: none"></select><br>

        <div id="toggles_div">
          <div id="autoCACHE_div">
            <h4>autoCACHE</h4>
            <label for="autoCACHE" id="autoCACHE_label" class="switch">
              <input type="checkbox" name="attributes[]" value="autoCACHE" id='autoCACHE' onclick="toggle()">
              <span class="slider round"></span>
            </label>
          </div>
          <div id="autoLASR_div">
            <h4>autoLASR</h4>
            <label for="autoLASR" id="autoLASR_label" class="switch">
              <input type="checkbox" name="attributes[]" value="autoLASR" id='autoLASR' onclick="toggle()">
              <span class="slider round"></span>
            </label>
          </div>
        </div>

        <div id="advanced_right" class="advanced" style="visibility: hidden">
          <label for="custom_metric_name">New Metric</label>
          <input type="text" name="custom_metric_name" id="custom_metric_name">
          <label for="keys_list">Keywords</label>
          <input type="text" name="keys_list" id="keys_list">
          <label for=unitOfMeasureID"">unitOfMeasureID</label>
          <input type="number" name="unitOfMeasureID" id="unitOfMeasureID">

        </div>
      </form>
      <br>
      <div id="buttons_parent_div">
        <div id='advanced_div' class="advanced" style="visibility: hidden">
          <button name="PXREF_button" id="PXREF_button" onclick="PXREF_button()">View PXREF</button><br>
          <button name="rebuild_PXREF_button" id="rebuild_PXREF_button" onclick="rebuild_PXREF()">Rebuild PXREF</button><br>
          <button name="building_info_button" id="building_info_button" onclick="building_info_button()">View Buildings</button><br>
        </div>
        <div id="buttons_div" style="display:none">
          <button name="bootstrap_button" id="bootstrap_button" onclick="bootstrap()">Bootstrap</button>
          <button name="delete_button" id="delete_button" onclick="del()">Delete</button>
        </div>
      </div>
    </div>
    <div id="body_right">
      <pre id="output"></pre>
      <div id="sql_output_div">
        <table id="sql_output"></table>
      </div>
    </div>
	</body>
</html>
