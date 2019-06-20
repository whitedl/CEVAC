<html>
<head>
  <title>Jonathan</title>
</head>
<body>


<?php
  include "config.php";
  // echo date("d");
  // if(isset($_POST['date'])) echo $_POST['date'];
  // if(isset($_POST['time'])) echo $_POST['time'];
  $hour = clean($_GET['hour']);
  $day = clean($_GET['day']);
  $month = clean($_GET['month']);
  $clouds = clean($_GET['clouds']);
  $temp = clean($_GET['temp']);
  $humidity = clean($_GET['humidity']);
  if(isset($_GET['hour'])){
    $jonathan = "sudo -u bmeares python3 /home/bmeares/CEVAC/prediction/predictor.py $hour $day $month $temp $humidity $clouds";
    $jonathan .= " 2>&1\n";
    // echo $jonathan;
    echo exec($jonathan);
  }

?>
</body>
</html>
