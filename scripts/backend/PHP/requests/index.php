<?php
include "/cevac/PHP/functions.php";

session_start();
if(isset($_SESSION['username'])){ header('Location: manage.php'); die(); }


if(isset($_POST['submit'])) {
    if($_POST['username'] == "" || $_POST['password'] == "") {
      $login_error = "One or more fields are missing.";
    }
    else {
      $check = user_pass_check($_POST['username'],$_POST['password']);
      if($check==0) {
        $login_error = "Incorrect username/password.";
      }
      else if($check==1){
        $_SESSION['username'] = $_POST['username'];
        $_SESSION['U_ID'] = get_U_ID($_SESSION['username']);
        login($_SESSION['U_ID']);
        $login_error = "U_ID is ".$_SESSION['U_ID'];
        header('Location: browse.php');
        die();
      }		
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>CEVAC Database Management</title>
<!--    <link rel="stylesheet" type="text/css" href="css/har.css">
-->
<!--    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
-->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="css/style.css">
	</head>

<body>
  <div id="container" class="card center" style="background: white; width: 400px;">
  <div class="card-body">

  <h1 class="card-title">Sign in</h1>
  <form method="post" action="index.php">
  
  <div id="login" style="">
    <label for="username" class="card-subtitle">Username:</label>
	  <input id="username_box" class="form-control" style="width: 100%" type="text" name="username"><br />
    <label for="password_box" class="card-subtitle">Password:</label>
		<input id="password_box" class="form-control" style="width: 100%" type="password" name="password"><br />
  </div>

  <div align="left" style="width: 50%; float: right; text-align: center">
    <button name="submit" class="btn btn-primary btn-lg" type="submit" style="float: right; margin: 0 auto;">Log In</button>
  </div>
  </form>
 
  <div id="make_account" style="margin-top: 70px;">
<!-- </p>
-->
    <?php
      if(isset($login_error))
       {  echo "<div id='passwd_result'><p style='color: black'>".$login_error."</p></div>";}
    ?>

  </div>

  </div>

  </div>



</body>

</html>

