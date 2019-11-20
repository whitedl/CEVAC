function toggle(){
  form_request('toggle.php');
}

function bootstrap(){
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

function reset_PXREF(){
  table = document.getElementById('sql_output');
  table.innerHTML = "";
  view = "View PXREF";
  pb = document.getElementById('PXREF_button');
  pb.innerHTML = view;
  document.getElementById('PXREF_div').style.display = 'none';
  document.getElementById('download_button_div').style.display = 'none';
}
function PXREF_button_click(){
  pb = document.getElementById('PXREF_button');
  document.getElementById('Age_text').value = 'PXREF';
  view = "View PXREF";
  update = "Update PXREF";
  if(pb.innerHTML == view){
    get_PXREF_html();
    // pb.innerHTML = update;
    reset_buttons(pb);
  } else{
    update_aliases();
    pb.innerHTML = view;
  }
  document.getElementById('PXREF_div').style.display = 'block';
  reset_buttons(pb);
}
function building_info_button_click(){
  button = document.getElementById('building_info_button');
  view = "View Buildings";
  update = "Update Buildings";
  form = document.getElementById('add_building_div');
  form.style.display = "block";
  reset_buttons(button);
  if(button.innerHTML == view){
    get_BUILDING_INFO_html();
    reset_buttons(button);
    button.innerHTML = update;
  } else{
    // update_aliases();
    button.innerHTML = view;
  }
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
function upload_xref_button_click(){
  input = $('#upload_xref');
  input.change(function(e){

    var fullPath = document.getElementById('upload_xref').value;
    if (fullPath) {
      var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
      var filename = fullPath.substring(startIndex);
      if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
        filename = filename.substring(1);
      }
      confirm_message = "Are you sure you want to upload " + filename + "?";
      if(confirm(confirm_message)){
        e.preventDefault();
        // var formData = new FormData();
        var formData = new FormData(document.getElementById('toggle'));
        formData.append('file', $('#upload_xref')[0].files[0]);

        $.ajax({
          url : 'console/upload_XREF.php',
          type : 'POST',
          data : formData,
          processData: false,  // tell jQuery not to process the data
          contentType: false,  // tell jQuery not to set contentType
            success : success_output
        });
      }
    }
  });

  $('#upload_xref').click();
}
function delete_building_link_click(BSN){
  confirm_message = "Are you sure you want to delete all tables with the BuildingSName " + BSN + "?";
  super_confirm = "Are you REALLY sure? (deleting every single table with BuildingSName " + BSN + ")";
  if(confirm(confirm_message)){
    if(confirm(super_confirm)){
      $.ajax({
        url : 'console/delete_building.php',
        type : 'POST',
        data : { BuildingSName : BSN },
        success : get_BUILDING_INFO_html
      });
    }
  }
}
function download_XREF_click(){
  $.ajax({
    url : 'console/download_XREF.php',
    type : 'GET',
    data: $('form').serialize(),
    success : success_PXREF_csv
    // success : function(data){
      // alert(data);
    // }
  });
}
function download_PXREF_click(){
  $.ajax({
    url : 'console/download_PXREF.php',
    type : 'GET',
    data: $('form').serialize(),
    success : success_PXREF_csv
  });
}
function download_BuildingKeySearch_click(){
  bk = document.getElementById('search_BuildingKey').value;
  $.ajax({
    url : 'console/download_BuildingKeySearch.php',
    type : 'GET',
    data: { BuildingKey: bk },
    success : success_BuildingKeySearch_csv
  });
}
function download_button_click(){
  $.ajax({
    url : 'console/download_table.php',
    type : 'GET',
    data: $('form').serialize(),
    success : success_table_csv
  });
}
function BuildingKey_search_button_click(){
  button = document.getElementById('BuildingKey_search_button');
  document.getElementById('BuildingKey_search_div').style.display = 'block';
  document.getElementById('output').innerHTML = "";
  document.getElementById('sql_output').innerHTML = "";
  reset_buttons(button);
}
function view_latest_button_click(){
  button = document.getElementById('view_latest_button');
  document.getElementById('download_button').innerHTML = 'Download LATEST';
  document.getElementById('download_button_div').style.display = 'block';
  document.getElementById('Age_text').value = 'LATEST';
  reset_buttons(button);
  get_latest_html();
}
function view_day_button_click(){
  button = document.getElementById('view_day_button');
  document.getElementById('download_button').innerHTML = 'Download DAY';
  document.getElementById('download_button_div').style.display = 'block';
  document.getElementById('Age_text').value = 'DAY';
  reset_buttons(button);
  get_day_html();
}
function alerts_report_button_click(){
  button = document.getElementById('alerts_report_button');

  reset_buttons(button);
}
function test_button_click(){
  console.log('test');
  // form_request('start_socket.php');
  $.ajax({
  type: 'POST',
  url: 'console/start_socket.php',
  data: $('form').serialize(),
  success: function(data){
    console.log(data);
    websocket();
    // success_output(data);
    // document.getElementById('output').innerHTML = data;
    }
  });
}
function view_stats_button_click(){
  button = document.getElementById('view_stats_button');
  // document.getElementById('download_button').innerHTML = 'Download LATEST';
  // document.getElementById('download_button_div').style.display = 'block';
  // document.getElementById('Age_text').value = 'LATEST';
  reset_buttons(button);
  get_stats_html();
}
