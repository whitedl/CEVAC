<head>
<title>CEVAC SQL</title>
<link rel="stylesheet" type="text/css" href="har.css">
</head>
<body>
  <div style="margin: 0 auto; width: 70%;">
  <h2>Query</h2>
    <form autocomplete="off" method='post' action='query_view.php'>
    <textarea style='width:100%; float: center' name='query' rows='6'
      autofocus
      maxlength='2000'
      onfocus="var val = this.value; this.value = ''; this.value = val; console.log(val)"
    ><?php if(isset($_POST['query'])) echo urldecode($_POST['query']); ?></textarea><br>
      <input type="submit" style="float: right">
    </form>
  </div>

  <iframe 
    style='width:100%; height:100%'
    frameborder="0"
    src="query.php?q=<?php if(isset($_POST['query'])) echo urlencode($_POST['query']); ?>"></iframe>


<?php
include "config.php";
global $db;

// $vars = json_decode(stripslashes(file_get_contents("php://input")), true);
// $query = $_GET['q'];


// $result = sqlsrv_query($db, $query);
// while($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)){
  // $json = json_encode($row);
  // echo $json;
// }


// while($row = sqlsrv_fetch_array($result)){
  // for($i = 0; $i < sizeof($row); $i++){
    // echo $row[$i]." ";
  // }
// }

// sqlsrv_close($db);
?>


</body>
