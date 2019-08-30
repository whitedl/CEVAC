<?php
$column = $_GET['c'];
$BuildingSName = $_GET['b'];
$Metric = $_GET['m'];
$TableName = $_GET['t'];
$value = $_GET['v'];

$exec = "/cevac/scripts/toggle_CEVAC_TABLES.sh -v $value -c $column";

if(!isset($_GET['t']) && (!isset($_GET['b']) || !isset($_GET['m']))) die('missing params');

if(isset($_GET['t'])){
  $exec .= " -t $TableName";
} else{
  $exec .= " -b $BuildingSName -m $Metric";
}

echo `$exec`;

?>
