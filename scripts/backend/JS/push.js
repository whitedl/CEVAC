function form_request(script){
  u = 'console/' + script;
  $.ajax({
    type: 'POST',
    url: u,
    data: $('form').serialize(),
    success: success_output
  });
}
function submit_table(TableName){
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
  u = 'console/html_to_table.php';
  fd = $('form').serializeArray();
  $.ajax({
    type: 'POST',
    url: u,
    data: { headers: headers, tdata: tdata , fd: fd, TableName: TableName},
    success: function(data){
      alert(data);
      // console.log(data);
    }
  });
}
function rebuild_PXREF_click(){
  exemptArray = [document.getElementById('output_text_div')];
  hide_output(exemptArray);
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
function push_to_lasr(){
  button = document.getElementById('push_to_lasr_button');
  button.disabled = true;
  reset_buttons(button);
  if(button.disabled){
    console.log('disabled');
    console.log(button);
  }
  BuildingSName = document.getElementById('buildings').value;
  Metric = document.getElementById('metrics').value;
  rebuild_csv = false

  $.ajax({
    type: 'POST',
    url: 'console/push_to_lasr.php',
    data: $('form').serialize(),
    success: function(data){
      button = document.getElementById('push_to_lasr_button');
      success_output(data);
      // document.getElementById('output').innerHTML = data;
      // reset_buttons(button);
      button.disabled = false;
      console.log(data);
    }
  });
  // form_request('push_to_lasr.php');
}
function kill_websocket(){
   $.ajax({
    type: 'POST',
    url: 'console/kill_websocket.php',
    data: $('form').serialize(),
    success: function(data){
      console.log(data);
    }
  });
}
