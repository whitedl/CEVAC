function get_html_update(b){
  get_Metrics_html(b);
}
function get_attributes_html(){
  b = document.getElementById('buildings').value
  m = document.getElementById('metrics').value
  reset_PXREF();

  attributes = ['autoCACHE', 'autoLASR'];
  attributes.forEach(function(item, index, array){
    $.get('console/bin_value.php', { BuildingSName: b, Metric: m, column: item}, function(data){
      document.getElementById(item + "_div").style.display = 'block';
      if(data == '1'){
        document.getElementById(item).checked = true;
      }
      else document.getElementById(item).checked = false;
    });
  });
}
function get_Metrics_html(){
  b = document.getElementById('buildings').value
  f = document.forms.toggle.actions_select.value
  $.get('console/metrics_html.php', { BuildingSName: b, filter: f }, function(data){
    metrics = document.getElementById('metrics');
    metrics.outerHTML = data;
    metrics.display = 'block';
    get_attributes_html(b,metrics.value)
  });
  show_buttons();
}
function get_BUILDING_INFO_html(){
  b = document.getElementById('buildings').value;
  m = document.getElementById('metrics').value;
  $.get('console/BUILDING_INFO_html.php', { BuildingSName: b, Metric: m }, function(data){
		document.getElementById('output').innerHTML = "";
    sql_out = document.getElementById('sql_output');
    sql_out.innerHTML = data;
  });
}
function get_PXREF_html(){
  b = document.getElementById('buildings').value;
  m = document.getElementById('metrics').value;
  PXREF = 'CEVAC_' + b + '_' + m + '_PXREF';
  $.get('console/table_exists.php',
    { TableName : PXREF },
    function(data){
      if(data == "DNE"){
        document.getElementById('download_PXREF_button').disabled = true;
        document.getElementById('output').innerHTML = PXREF + ' does not exist. Click \"Rebuild PXREF\" to create the PXREF.';
      } else {
        document.getElementById('download_PXREF_button').disabled = false;
        $.get('console/PXREF_html.php', $('form').serialize(), function(data){
          document.getElementById('output').innerHTML = "";
          sql_out = document.getElementById('sql_output');
          sql_out.innerHTML = data;
        });
      }
    }
  );


}
function get_BuildingKeySearch_html(){
  b = document.getElementById('buildings').value;
  m = document.getElementById('metrics').value;
  bk = document.getElementById('search_BuildingKey').value;
  $.get('console/BuildingKeySearch_html.php', { BuildingSName: b, Metric: m, BuildingKey: bk }, function(data){
		document.getElementById('output').innerHTML = "";
    sql_out = document.getElementById('sql_output');
    sql_out.innerHTML = data;
  });
}
function success_PXREF_csv(data){
  var datetime = new Date().getTime();
  filename = String(datetime) + '_' + data.substring(4, data.length);
  var element = document.createElement('a');
  element.setAttribute('href',data);
  element.setAttribute('download',filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);

}
function success_BuildingKeySearch_csv(data){
  var datetime = new Date().getTime();
  filename = String(datetime) + '_' + data.substring(4, data.length);
  var element = document.createElement('a');
  element.setAttribute('href',data);
  element.setAttribute('download',filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);

}
function success_table_csv(data){
  var datetime = new Date().getTime();
  filename = String(datetime) + '_' + data.substring(4, data.length);
  var element = document.createElement('a');
  element.setAttribute('href',data);
  element.setAttribute('download',filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}
function table_exists(tn){
  $.get('console/table_exists.php',
    { TableName : tn },
    function(data){

    }
  );
}
function get_latest_html(){
  button = document.getElementById('view_latest_button');
  button.classList.add('disabled');
  button.disabled = true;
  $.get('console/table_html.php',
    $('form').serialize(),
    function(data){
      document.getElementById('sql_output').innerHTML = data;
      button.disabled = false;
      button.classList.remove('disabled');
    }
  );
}
function get_day_html(){
  button = document.getElementById('view_day_button');
  button.classList.add('disabled');
  button.disabled = true;
  $.get('console/table_html.php',
    $('form').serialize(),
    function(data){
      document.getElementById('sql_output').innerHTML = data;
      button.disabled = false;
      button.classList.remove('disabled');
    }
  );
}
function websocket(){
  // helper function: log message to screen
  function log(msg) {
    document.getElementById('output').textContent += msg + '\n';
  }

  // setup websocket with callbacks
  var ws = new WebSocket('ws://wfic-cevac1:8080/');
  ws.onopen = function() {
    log('CONNECT');
  };
  ws.onclose = function() {
    log('DISCONNECT');
    kill_websocket();
  };
  ws.onmessage = function(event) {
    log('MESSAGE: ' + event.data);
  };
}
