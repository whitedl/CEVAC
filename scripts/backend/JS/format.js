function show_hide(id){
  element = document.getElementById(id);
  if(element.style.display == "none") element.style.display = "block";
  else element.style.display = "none";
}
function show_hide_class(c){
  elements = document.getElementsByClassName(c);
  for(var i = 0; i < elements.length; i++)
    if(elements[i].style.visibility == "hidden") elements[i].style.visibility = "visible";
    else elements[i].style.visibility = "hidden";
}
function reset_buttons(active_button = ""){
  // active_button = document.getElementById(active);
  PXREF_button = document.getElementById('PXREF_button');
  upload_xref_button = document.getElementById('upload_xref_button');
  rebuild_PXREF_button = document.getElementById('rebuild_PXREF_button');
  building_info_button = document.getElementById('building_info_button');
  add_building_button = document.getElementById('add_building_button');
  console.log('reset');

  if(PXREF_button != active_button){
    PXREF_button.innerHTML = 'View PXREF';
    document.getElementById('PXREF_div').style.display = 'none';
  }
  if(rebuild_PXREF_button != active_button) rebuild_PXREF_button.innerHTML = 'Rebuild PXREF';
  if(upload_xref_button != active_button) upload_xref_button.innerHTML = 'Upload XREF';
  if(building_info_button != active_button){
    building_info_button.innerHTML = 'View Buildings';
    document.getElementById('add_building_div').style.display = "none";
  }
}
