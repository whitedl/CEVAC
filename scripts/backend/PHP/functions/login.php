<?php
function user_pass_check($username, $password){
  global $db;
	
	$query = "SELECT password_hash FROM CEVAC_USERS WHERE username ='$username'";
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
  $_SESSION['username'] = get_username($U_ID);
}

function enforce_login(){
  if(!isset($_SESSION['username']) || !isset($_SESSION['U_ID'])){
    header("Location: index.php");
    die();
  }
}
function user_exists($username){
  $query = "
  IF EXISTS(SELECT username FROM CEVAC_USERS WHERE username = '$username') SELECT 'exists'
  ELSE SELECT 'dne';
  ";
  $exists = sql_value($query);
  if($exists == "exists") return True;
  else return False;
}
function register_user($username, $U_type, $password_hash, $email){
  if(user_exists($username)) return False;
  $query = "
  INSERT INTO CEVAC_USERS(
    U_type, email, password_hash, username
  ) VALUES (
    '$U_type', '$email', '$password_hash', '$username'
  );
  ";
  exec_sql($query);
  return True;
}
function get_U_ID($username){
  $query = "
  SELECT U_ID FROM CEVAC_USERS
  WHERE username = '$username';
  ";
  return sql_value($query);
}
function get_username($U_ID){
  $query = "
  SELECT username FROM CEVAC_USERS
  WHERE U_ID = $U_ID;
  ";
  return sql_value($query);
}

?>
