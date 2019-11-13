<?php
session_start();

include_once "../functions.php";

if(isset($_POST['submit'])) {
  if($_POST['username'] == "" || $_POST['password'] == ""
    || $_POST['confirm_password'] == "" || $_POST['email'] == ""  
  ) {
    $login_error = "Please enter all fields!";
  } else if($_POST['password'] != $_POST['confirm_password']){
    $login_error = "Password fields do not match.";
  } else{
      if(user_exists(clean($_POST['username']))) $login_error = "Username taken.";
      else{
        $username = clean($_POST['username']);
        $password_hash = password_hash($_POST['password'], PASSWORD_DEFAULT);
        $U_type = "1";
        $email = $_POST['email'];
        
        $check = register_user($username, $U_type, $password_hash, $email);
        if($check){
          login(get_U_ID($username));
          header("Location: manage.php");
          die();
        } else{
          $login_error = "Unable to log in";
        }
      }
  }
}

?>
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

<div class="container">
  <h1>Register</h1>
  <div class="row">
  <form action="register.php" method="post">
    <div class="col-sm-4">
      <h3>Username: </h3>
      <input type="text" name="username">
    </div>

    <div class="col-sm-4">
      <h3>Email: </h3>
      <input type="email" name="email">
      <br><h3>Password: </h3>
      <input class="text" type="password" name="password"><br>
      <h3>Confirm Password: </h3>
      <input class="text" type="password" name="confirm_password"><br><br>
      <input class="btn btn-primary" type="submit" value="Submit" name="submit">
    </div>
  </form>
<?php
  if(isset($login_error))
   {  echo "<div id='passwd_result'><p>".$login_error."</p></div>";}
?></div>
</div>

</body>

</html>


