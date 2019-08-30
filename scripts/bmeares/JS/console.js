function toggle(){
  var formData = document.getElementById('toggle');

  b_index = formData.buildings.selectedIndex;
  BuildingDName = formData.buildings[b_index].text;
  BuildingSName = formData.buildings[b_index].value;

  m_index = formData.metrics.selectedIndex;
  Metric = formData.metrics[m_index].value;

  attributes = formData.attributes;
  autoCACHE = 0;
  autoLASR = 0;
  if(attributes[0].checked) autoCACHE = 1;
  if(attributes[1].checked) autoLASR = 1;

  url = "console/toggle.php?b=" + BuildingSName + "&m=" + Metric;
  url += "&"
  console.log(url);

  // $.post(url,"", success_output);
  output.innerHTML = "CEVAC_" + BuildingSName + "_" + Metric;
}

function success_output(data){
  output = document.getElementById('output');
  output.innerHTML = data;
  console.log(data);
}
