<head>
<title>CEVAC SQL</title>
</head>
<body>
  <div style="margin: 0 auto; width: 70%;">
  <h2>Reload Cache</h2>
    <form autocomplete="off" method='post' action=''>
    <h3><i>Type the table to update</i></h3>
    <textarea style='width:100%; float: center' name='table' rows='1'
      autofocus
      maxlength='2000'
      onfocus="var val = this.value; this.value = ''; this.value = val; console.log(val)"
    ><?php if(isset($_POST['table'])) echo $_POST['table']; ?></textarea><br>
    <input type='radio' name='INIT_APPEND' value='APPEND' <?php echo ($_POST['INIT_APPEND'] != 'INIT' ? 'checked' : '')?>>Create/append to cache
      <input type='radio' name='INIT_APPEND' value='INIT' <?php echo ($_POST['INIT_APPEND'] == 'INIT' ? 'checked' : '') ?>>Drop and rebuild cache
      <input type="submit" style="float: right">
    </form>
  </div>


  <iframe 
    style='width:100%; height:100%'
    frameborder="0"
    src="query.php?q=<?php
    if(isset($_POST['table'])){
      $query = "EXEC CEVAC_CACHE_".$_POST['INIT_APPEND']." @tables = '".$_POST['table']."'";
      echo urlencode($query);
    }
    ?>"></iframe>

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
