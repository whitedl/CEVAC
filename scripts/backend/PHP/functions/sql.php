<?php

function exec_sql($query){
  global $db;
  $result = sqlsrv_query($db, $query);
  if($result === false) die(print_r(sqlsrv_errors(), true));
  return $result;
}
function sql_value($query){
  $result = exec_sql($query);
  $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_NUMERIC);
  if($row === false) die(print_r(sqlsrv_errors(), true));
  return $row[0];
}
function table_exists($tablename){
  $query = "IF OBJECT_ID('$tablename') IS NOT NULL SELECT 'EXISTS' AS 'e' ELSE SELECT 'DNE' AS 'e';";
  $e = sql_value($query);
  return ($e == "EXISTS");
}
function get_columns($TableName){
  $query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$TableName'";
  return exec_sql($query);
}
?>
