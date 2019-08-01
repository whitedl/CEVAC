<?php
include "../config.php";
include "../db.php";
function get_RecordTypes(){
  global $db;
  $query = "SELECT DISTINCT a.RecordType FROM AOL_2019 AS a
   ORDER BY RecordType";
  $result = $db->query($query);
  $out = '';
  while ($row = mysqli_fetch_row($result)){ $out .= '<option value="'.$row[0].'">'.$row[0].'</option>'; }
  return $out;
}
function get_Chapters(){
  global $db;
  $query = "SELECT DISTINCT Chapter FROM AOL_2019 WHERE Chapter IS NOT NULL ORDER BY Chapter";
  $result = $db->query($query);
  $out = '';
  while ($row = mysqli_fetch_row($result)){ $out .= '<option value="'.$row[0].'">'.$row[0].'</option>'; }
  return $out;
}

function generate_csv($query){
  global $db;
  $t = strval(time());

  $q_array = explode("ORDER", $query);
  $q_clean = $q_array[0];
  $db->query("INSERT INTO TEMP(TEMP) VALUES ('$q_clean')");
  $headers = "";
  $view_query = "CREATE VIEW AOL_TEMP_$t AS ( SELECT * FROM ($q_clean) AS q LIMIT 1 );";
  $db->query($view_query);
  $h_query = "SELECT COLUMN_NAME AS 'Field' FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'AOL' AND TABLE_NAME = 'AOL_TEMP_$t';";
  $result = $db->query($h_query);
  while($row = mysqli_fetch_row($result)) $headers .= "'".$row[0]."',";
  $headers = substr($headers, 0, -1);
  $db->query("DROP VIEW AOL_TEMP_$t");

  $datacsv = $t."_data.csv";
  $outputcsv = $t."_output.csv";
  $colscsv = $t."_cols.csv";
  $cleanup = "sudo -u master rm -f /home/master/AOL/public/csv/*.csv &&\\
    sudo -u master ssh master@node1 'sudo rm -f /var/lib/mysql-files/*.csv'";
  exec($cleanup);
  $out_query = "SELECT * INTO OUTFILE '/var/lib/mysql-files/$datacsv'
  FIELDS TERMINATED BY '|'
  OPTIONALLY ENCLOSED BY ''
  LINES TERMINATED BY '\\r\\n' FROM ($query) AS original;
";
  $h_query = "SELECT * INTO OUTFILE '/var/lib/mysql-files/$colscsv'
  FIELDS TERMINATED BY '|'
  OPTIONALLY ENCLOSED BY ''
  LINES TERMINATED BY '\\r\\n' FROM (SELECT $headers) AS headers;
";

  $db->query($h_query);
  $db->query($out_query);
  // echo "$out_query";

  $move_files = "
  sudo -u master ssh master@node1 'sudo mv /var/lib/mysql-files/$datacsv /home/master/newdrive/csv/$datacsv'
  sudo -u master ssh master@node1 'sudo mv /var/lib/mysql-files/$colscsv /home/master/newdrive/csv/$colscsv'
  sudo -u master ssh master@node1 'sudo cat /home/master/newdrive/csv/$colscsv /home/master/newdrive/csv/$datacsv | sponge /home/master/newdrive/csv/$outputcsv'
";
  exec($move_files);
  return $outputcsv;
}

function gen_sql($post){
  $query = "";
  $cols = ""; $where = ""; $order = ""; $headers = "";
  if(!empty($post['include'])){
    foreach($post['include'] as $col){
      $cols .= "COALESCE($col, 'No $col available') AS $col,";
      $headers .= "'$col',";
    }
  } else die();
  if(!empty($post['where'])){
    $i = 0;
    foreach($post['where'] as $col){
      if(!isset($post["". $col.""])) $k = '%';
      else $k = "\\".str_replace("%", "\\%", strval($post["".$col.""])."");
      $where .= " $col LIKE '%".$k."%' AND";
      $i++;
    }
  } else $where = '1 AND';
  $cols = substr($cols, 0, -1);
  $headers = substr($headers, 0, -1);
  $where = substr($where, 0, -4);
  if(isset($post['order'])) $order = "ORDER BY ".$post['order']." ASC";
  $query = "SELECT $cols FROM AOL_2019 WHERE $where $order";
  return $query;
}

?>
