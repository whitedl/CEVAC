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

function clean($string) {
  $string = str_replace(' ', '', $string); // Replaces all spaces with hyphens.
  return preg_replace('/[^A-Za-z0-9.\-]/', '', $string); // Removes special chars.
}


?>
