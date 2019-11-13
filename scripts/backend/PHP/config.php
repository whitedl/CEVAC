<?php

$serverName = "130.127.218.11";
$connectionInfo = array( "Database"=>"WFIC-CEVAC",
  "UID"=>"wficcm", 
  "PWD"=>"5wattcevacmaint$",
  "ReturnDatesAsStrings"=>true
);
$db = sqlsrv_connect( $serverName, $connectionInfo);

if( $db ) {
       // echo "Connection established.<br />";
}else{
       echo "Connection could not be established.<br />";
       die( print_r( sqlsrv_errors(), true));
}

function clean($string, $exclude_array = []) {
  // $string = str_replace(' ', '', $string); // Replaces all spaces with hyphens.
  $array = ['A-Z','a-z','0-9','-', '_'];
  $array = array_merge($array, $exclude_array);
  $r = '/[^';
  foreach($array as &$w){ $r .= $w; }
  $r .= ']/';
  return preg_replace($r, '', $string); // Removes special chars.
}


?>
