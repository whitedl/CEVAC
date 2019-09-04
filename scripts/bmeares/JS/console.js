function form_request(script){
  u = 'console/' + script;
  $.ajax({
    type: 'POST',
    url: u,
    data: $('form').serialize(),
    success: success_output
  });
}
function toggle(){
  form_request('toggle.php');
}
let del = () =>{
  button = document.getElementById('delete_button');
  button.disabled = true;
  $.ajax({
    type: 'POST',
    url: 'console/delete.php',
    data: $('form').serialize(),
    success: function(data){
      document.getElementById('delete_button').disabled = false;
      document.getElementById('output').innerHTML = data;
    }
  });
}
let bootstrap = () =>{
  button = document.getElementById('bootstrap_button');
  button.disabled = true;
  $.ajax({
    type: 'POST',
    url: 'console/bootstrap.php',
    data: $('form').serialize(),
    success: function(data){
      document.getElementById('bootstrap_button').disabled = false;
      document.getElementById('output').innerHTML = data;
    }
  });
}
function get_html_update(b){
  get_Metrics_html(b);
}

function get_attributes_html(){
  b = document.getElementById('buildings').value
  m = document.getElementById('metrics').value

  // form = document.getElementById('toggle');
  // attributes = [];

  // form.elements["attributes[]"].forEach(function(item, index, array){
    // attributes.push(item.value);
  // });
  // console.log(attributes);

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
function get_PXREF_html(){
  b = document.getElementById('buildings').value;
  m = document.getElementById('metrics').value;
  $.get('console/PXREF_html.php', { BuildingSName: b, Metric: m }, function(data){
		document.getElementById('output').innerHTML = "";
    sql_out = document.getElementById('sql_output');
    sql_out.innerHTML = data;
  });
}


function show_buttons(){
  d = document.getElementById('buttons_div');
  d.style.display = 'block';
}
function success_output(data){
  output = document.getElementById('output');
  output.innerHTML = data;
}

