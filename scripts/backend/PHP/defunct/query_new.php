<html>
<head>
<title>CEVAC Query Debugger</title>
<link rel="stylesheet" type="text/css" href="har.css">
<script src="https://code.jquery.com/jquery-1.11.0.min.js"></script>
<script src="misc.js"></script>
</head>

<body onload="enable_submit()">
  <div style="margin: 0 auto; width: 70%;">
    <h2>Query Debugger</h2>
    <form autocomplete="off" method='post' action="query_new.php" id="form" >
     
      <textarea oninput="enable_submit()" style="width:100%; float: center; display: block;" name='query_box' id = 'query_box' rows='6' autofocus maxlength='2000'
      onfocus="var val = this.value; this.value = ''; this.value = val;"
    ><?php if(isset($_POST['query_box'])) echo urldecode($_POST['query_box']); ?></textarea>

    <input id = 'submit' type="submit" style="float: right" name = 'submit'>
    </form>
  </div>

<?php if(isset($_POST['submit'])){
  include "../config.php";
  global $db;
  if(!isset($_POST['query_box'])) $query = gen_sql($_POST);
  else $query = $_POST['query_box'];

  $result = sqlsrv_query($db, "WITH q AS ($query) SELECT COUNT(*) FROM q");
  $row = sqlsrv_fetch_array($result, SQLSRV_FETCH_NUMERIC);
  $rc = $row[0];
  
  echo "<p>Results: $rc</p>";
  echo "<table>\n";

  if(!empty($_POST['include'])){
    foreach($_POST['include'] as $col){
      echo "\t<th>$col</th>";
    }
  }

  $result = sqlsrv_query($db, $query);
  while ($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
      echo "\t<tr>\n";
      foreach($row as $row_value){
          echo "\t\t<td>$row_value</td>\n";
      }
      echo "\t</tr>\n";
  }
  echo "</table>\n";
  }
  sqlsrv_close($db);
  ?>

</body>
</html>
