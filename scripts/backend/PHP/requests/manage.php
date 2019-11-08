<?php
  include "../functions.php";
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
	<body onload="get_Metrics_html(); enable_BuildingKeySearch()" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
    <h2>CEVAC Administrative Console</h2>
    <!-- <a onclick="show_hide_class('advanced');" href="#">Advanced options</a><br><br> -->
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
        <input type="text" id="Age_text" name="Age">
        <input type="file" name="upload_xref" id="upload_xref" />
        <div id="select_options_div">
          <?php echo buildings_html(); ?>
          <select name="Metric" id="metrics" style="display: none"></select><br>
        </div>
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

        <div id="advanced_right" class="advanced">
<!--          <label for="custom_metric_name">New Metric</label>
          <input type="text" name="custom_metric_name" id="custom_metric_name">
          <label for="keys_list">Keywords</label>
          <input type="text" name="keys_list" id="keys_list">
          <label for=unitOfMeasureID"">unitOfMeasureID</label>
          <input type="number" name="unitOfMeasureID" id="unitOfMeasureID">
-->
        </div>
      </form>
      <br>
      <div id="buttons_parent_div">
        <div id='advanced_div' class="advanced">
          <h5>Table Actions</h5>
          <ul id="table_actions_list">
            <li><a href="#" id="view_latest_button" onclick="view_latest_button_click()">View Latest</a></li>
            <li><a href="#" id="view_day_button" onclick="view_day_button_click()">View Last 24 Hours</a></li>
          </ul>
          <h5>XREF Actions</h5>
          <ul id="XREF_list">
            <li><a href="#" id="PXREF_button" onclick="PXREF_button_click()">View PXREF</a></li>
            <li><a href="#" name="rebuild_PXREF_button" id="rebuild_PXREF_button" onclick="rebuild_PXREF_click()">Rebuild PXREF</a></li>
            <li><a href="#" name="upload_xref_button" id="upload_xref_button" onclick="upload_xref_button_click()">Upload XREF</a></li>
          </ul>
          <h5>Building Actions</h5>
          <ul id="building_info_list">
            <li><a href="#" name="building_info_button" id="building_info_button" onclick="building_info_button_click()">View Buildings</a></li>
            <li><a href="#" name="BuildingKey_search_button" id="BuildingKey_search_button" onclick="BuildingKey_search_button_click()">Search BuildingKeys</a></li>
          </ul>
<!--          <h5>Alerts Actions</h5>
          <ul id="alerts_list">
            <li><a href="#" name="alerts_report_button" id="alerts_report_button" onclick="alerts_report_button_click()">Generate Alerts Report</a></li>
          </ul>
-->
<!--          <button name="PXREF_button" id="PXREF_button" onclick="PXREF_button_click()">View PXREF</button><br> -->
<!--          <button name="rebuild_PXREF_button" id="rebuild_PXREF_button" onclick="rebuild_PXREF_click()">Rebuild PXREF</button><br>
          <button name="upload_xref_button" id="upload_xref_button" onclick="upload_xref_button_click()">Upload XREF</button><br>
          <button name="building_info_button" id="building_info_button" onclick="building_info_button_click()">View Buildings</button><br>
          <button name="BuildingKey_search_button" id="BuildingKey_search_button" onclick="BuildingKey_search_button_click()">Search BuildingKeys</button><br>
-->
        </div>
        <div id="buttons_div">
          <div id="buttons_div_left" style="float: left;">
            <button class="action_button" name="bootstrap_button" id="bootstrap_button" onclick="bootstrap()">Build Pipeline</button>
            <button class="action_button" name="push_to_lasr_button" id="push_to_lasr_button" onclick="push_to_lasr()">Push to LASR</button>
            <button class="action_button" name="websocket_button" id="websocket_button" onclick="test_button_click()">Websocket</button>
          </div>
          <div id="buttons_div_right" style="float: right;">
            <button class="action_button" name="delete_button" id="delete_button" onclick="del()">Delete</button>
          </div>
        </div>
      </div>
    </div>
    <div id="body_right">
      <div id="BuildingKey_search_div">
        <input placeholder="BuildingKey" type="text" id="search_BuildingKey" oninput="enable_BuildingKeySearch()">
        <button onclick="get_BuildingKeySearch_html()" id="BuildingKeySearch_submit_button">Search</button>
        <button onclick="download_BuildingKeySearch_click()" id="BuildingKeySearch_download_button">Download</button>
      </div>
      <div id="PXREF_div">
        <button onclick='download_PXREF_click()' id="download_PXREF_button">Download PXREF</button>
        <button onclick='download_XREF_click()' id="download_XREF_button">Download XREF</button>
      </div>
      <div id="download_button_div">
        <button onclick='download_button_click()' id="download_button">Download</button>
      </div>
      <div id="add_building_div">
        <form id="add_building_form">
          <input placeholder="BuildingSName" type="text" id="new_BuildingSName" name="new_BuildingSName"/>
          <input placeholder="BuildingDName" type="text" id="new_BuildingDName" name="new_BuildingDName"/>
          <input placeholder="BuildingKey" type="text" id="new_BuildingKey" name="new_BuildingKey"/>
        </form>
        <button id="add_building_button" onclick="add_building_click()">Add Building</button>
      </div>
      <pre id="output"></pre>
      <div id="sql_output_div">
        <table id="sql_output"></table>
      </div>
    </div>
	</body>
</html>
