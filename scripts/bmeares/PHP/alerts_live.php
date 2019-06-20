<?php

session_start();
include "config.php";
global $db;
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');

// session time is out of date. Send alerts as event
if(!isset($_SESSION['time']) || $_SESSION['time'] < $newest_time){


}

fire_event();

// Initialize session time on first run
if(!isset($_SESSION['time'])) $_SESSION['time'] = time();


sqlsrv_close($db);


/*
 * fire_event()
 * Fires an event for event listeners
 * 
 * */

function fire_event(){
  $newest_query = 'SELECT TOP 1 dbo.ConvertUTCToLocal(BeginTime) AS BeginTimeET
    FROM CEVAC_ALL_ALERTS_HIST ORDER BY BeginTime DESC';
  $newest_result = sqlsrv_query($db, $newest_query);
  $newest_row = sqlsrv_fetch_array($newest_result, SQLSRV_FETCH_ASSOC);
  $newest_time = strtotime($newest_row['BeginTimeET']);

  $_SESSION['time'] = time();
  $query = '
    SELECT AlertID, RTRIM(AlertType) AS AlertType, RTRIM(AlertMessage) AS AlertMessage,
    RTRIM(Metric) AS Metric, RTRIM(BLDG) AS BLDG, Acknowledged, BeginTime, EndTime
    FROM CEVAC_ALL_ALERTS_HIST
    WHERE Acknowledged = 0
    ORDER BY AlertID DESC;
  ';

  $array = array();


  $result = sqlsrv_query($db, $query);
  while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
    $array[] = $row;
  }

  $out = json_encode($array);
  echo "data: ".$out."\n\n";
  flush();


}



?>

