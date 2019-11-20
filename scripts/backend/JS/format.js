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
  BuildingKey_search_button = document.getElementById('BuildingKey_search_button');
  download_button = document.getElementById('download_button');
  view_latest_button = document.getElementById('view_latest_button');
  view_stats_button = document.getElementById('view_stats_button');
  view_day_button = document.getElementById('view_day_button');
  document.getElementById('output').innerHTML = '';
  document.getElementById('canvas_div').style.display = "hidden";
  // console.log('reset');

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
  if(BuildingKey_search_button != active_button){
    document.getElementById('BuildingKey_search_div').style.display = "none";
  }
  if(download_button != active_button && view_latest_button != active_button &&
  view_day_button != active_button){
    document.getElementById('download_button_div').style.display = 'none';
  }
}
function enable_BuildingKeySearch(){
  console.log('hm');
  sbutton = document.getElementById('BuildingKeySearch_submit_button');
  dbutton = document.getElementById('BuildingKeySearch_download_button');
  input = document.getElementById('search_BuildingKey');
  if(input.value.length > 0){
    sbutton.disabled = false;
    // sbutton.style.color = 'green';
    dbutton.disabled = false;
    // dbutton.style.color = 'green';
  } else{
    sbutton.disabled = true;
    dbutton.disabled = true;
  }
}

function plot(data){
  document.getElementById('canvas_div').style.display = 'block';
  let jsonfile = JSON.parse(data);
  var labels = jsonfile.map(function(e) {
     return e.Alias;
  });
  var data = jsonfile.map(function(e) {
     return e.ActualValue;
  });;

  var BuildingSName = document.getElementById('buildings').value;
  var Metric = document.getElementById('metrics').value;
  var Age = document.getElementById('Age_text').value;
  var TableName = 'CEVAC_' + BuildingSName + '_' + Metric + '_' + Age;
  var ctx = canvas.getContext('2d');
  ctx.fillStyle = 'black';
  var config = {
     type: 'bar',
     data: {
        labels: labels,
        datasets: [{
           label: TableName,
           data: data,
           backgroundColor: 'rgba(0, 119, 204, 0.3)'
        }]
     },
    options: {
      legend: {
        labels: {
          fontColor: "#FFFFFF"
        }
      },
      scales: {
        // fontColor: "#FFFFFF"
        yAxes: [{
          ticks: {
            fontColor: "#FFFFFF"
          }
        }],
        xAxes: [{
          ticks: {
            fontColor: "#FFFFFF"
          }
        }]
      }
    }
  };

  var chart = new Chart(ctx, config);
  console.log('wut');
}

