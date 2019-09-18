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
function rebuild_PXREF(){
  form_request('rebuild_PXREF.php');
  document.getElementById('PXREF_button').innerHTML = "View PXREF";
}
function del(){
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
