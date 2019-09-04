function show_hide(id){
  element = document.getElementById(id);
  if(element.style.display == "none") element.style.display = "block";
  else element.style.display = "none";
}
function show_hide_class(c){
  elements = document.getElementsByClassName(c);
  for(var i = 0; i < elements.length; i++)
    if(elements[i].style.display == "none") elements[i].style.display = "block";
    else elements[i].style.display = "none";
}
