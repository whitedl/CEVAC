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
  $.get('console/PXREF_html.php', { BuildingSName: b, Metric: m }, function(data){
		document.getElementById('output').innerHTML = "";
    sql_out = document.getElementById('sql_output');
    sql_out.innerHTML = data;
  });
}
function success_PXREF_csv(data){
  alert(data);
  var datetime = new Date().getTime();
  filename = String(datetime) + '_' + data.substring(4, data.length);

  console.log(data);
  var element = document.createElement('a');
  element.setAttribute('href',data);
  element.setAttribute('download',filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);

}
