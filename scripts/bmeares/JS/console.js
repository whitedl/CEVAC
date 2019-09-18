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
function building_info_button(){
  button = document.getElementById('building_info_button');
  view = "View Buildings";
  update = "Update Buildings";
  if(button.innerHTML == view){
    get_BUILDING_INFO_html();
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
function upload_xref_button(e){
  $('#upload_xref').click();
  e.preventDefault();
}
