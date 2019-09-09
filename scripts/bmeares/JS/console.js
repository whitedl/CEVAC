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
  reset_PXREF();

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
function reset_PXREF(){
  table = document.getElementById('sql_output');
  table.innerHTML = "";
  view = "View PXREF";
  pb = document.getElementById('PXREF_button');
  pb.innerHTML = view;
}
function PXREF_button(){
  pb = document.getElementById('PXREF_button');
  view = "View PXREF";
  update = "Update PXREF";
  if(pb.innerHTML == view){
    get_PXREF_html();
    pb.innerHTML = update;
  } else{
    update_aliases();
    pb.innerHTML = view;
  }
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
  console.log(data);
}
function update_aliases(){
  table = document.getElementById('sql_output');
  headers = [];
  tdata = [];
  for(var i = 0, n = table.rows[0].cells.length; i < n; i++) headers.push(table.rows[0].cells[i].innerHTML);

  for(var r = 1, n = table.rows.length; r < n; r++) {
    row = [];
    for(var c = 0, m = table.rows[r].cells.length; c < m; c++) {
      row.push(table.rows[r].cells[c].innerHTML);
    }
    tdata.push(row);
  }
  send_xref(headers, tdata);
}
function send_xref(l,t){
  console.log('sending request');
  u = 'console/update_XREF.php';
  fd = $('form').serializeArray();
  // console.log(fd);
  // fd = document.getElementById('toggle');
  // for(var i = 0; i < l.length; i++) fd.append('headers[]', l[i]);
  // d = fd + $(l).serializeArray() + $(t).serializeArray();
  $.ajax({
    type: 'POST',
    url: u,
    data: { headers: l, tdata: t , fd: fd},
    // data: { fd },
    // data: { d },
    success: success_output
  });
}
function rebuild_PXREF(){
  form_request('rebuild_PXREF.php');
  document.getElementById('PXREF_button').innerHTML = "View PXREF";
}
