function form_request(script){
  u = 'console/' + script;
  $.ajax({
    type: 'POST',
    url: u,
    data: $('form').serialize(),
    success: success_output
  });
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
  $.ajax({
    type: 'POST',
    url: u,
    data: { headers: l, tdata: t , fd: fd},
    success: success_output
  });
}
function rebuild_PXREF_click(){
  form_request('rebuild_PXREF.php');
  reset_buttons();
  // get_PXREF_html();
}
function del(){
  button = document.getElementById('delete_button');
  button.disabled = true;
  b = document.getElementById("buildings").value;
  m = document.getElementById("metrics").value;
  confirm_message = "Are you sure you want to delete " + b + "_" + m + "?";
  if(confirm(confirm_message)){
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
}
function add_building_click(){
  button = document.getElementById('add_building_button');
  console.log('click');
  $.ajax({
    type: 'POST',
    url: 'console/add_building.php',
    data: $('form').serialize(),
    success: function(data){
      console.log(data);
      get_BUILDING_INFO_html();
      reset_buttons(button);
      document.getElementById('add_building_div').style.display = "block";
    }
  });
  // form_request('add_building.php');
}
