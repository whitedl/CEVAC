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
  form_request('delete.php');
}
let bootstrap = () =>{
  form_request('bootstrap.php');
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
  f = document.getElementById('actions_select').value
  $.get('console/metrics_html.php', { BuildingSName: b, filter: f }, function(data){
    metrics = document.getElementById('metrics');
    metrics.outerHTML = data;
    metrics.display = 'block';
    get_attributes_html(b,metrics.value)
  });
  show_buttons();
}
function show_buttons(){
  d = document.getElementById('buttons_div');
  d.style.display = 'block';
}
function success_output(data){
  output = document.getElementById('output');
  output.innerHTML = data;
}

