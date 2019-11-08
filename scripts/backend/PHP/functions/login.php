<?php
function user_pass_check($username, $password){
  global $db;
	
	$query = "SELECT password_hash FROM CEVAC_USERS WHERE U_name ='$username'";
  $password_hash = sql_value($query);
		
  if(password_verify($password, $password_hash)) return 1; //corect password
  else return 0; //incorrect
}


function check_logout(){
  if(isset($_GET['logout'])) logout();
}

function logout(){
	if(isset($_SESSION['username'])){
		unset($_SESSION['username']);
		unset($_SESSION['U_ID']);
	}
	header('Location: index.php');
}

function login($U_ID){
  $_SESSION['U_ID'] = $U_ID;
  $_SESSION['username'] = get_U_name($U_ID);
  $_SESSION['F_name'] = get_attribute($U_ID, "F_name");
  $_SESSION['L_name'] = get_attribute($U_ID, "L_name");
}

function enforce_login(){
  if(!isset($_SESSION['username']) || !isset($_SESSION['U_ID'])){
    header("Location: index.php");
    die();
  }
}

?>
