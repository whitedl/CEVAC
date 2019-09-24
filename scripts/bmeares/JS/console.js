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
}
function PXREF_button_click(){
  pb = document.getElementById('PXREF_button');
  view = "View PXREF";
  update = "Update PXREF";
  if(pb.innerHTML == view){
    get_PXREF_html();
    pb.innerHTML = update;
  reset_buttons();  } else{
    update_aliases();
    pb.innerHTML = view;
  }
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
    e.preventDefault();
    var formData = new FormData();
    formData.append('file', $('#upload_xref')[0].files[0]);

    $.ajax({
      url : 'console/upload_XREF.php',
      type : 'POST',
      data : formData,
      processData: false,  // tell jQuery not to process the data
      contentType: false,  // tell jQuery not to set contentType
        success : success_output
    });
  });

  $('#upload_xref').click();
}
