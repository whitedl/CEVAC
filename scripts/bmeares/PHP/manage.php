<?php
  include "functions.php";
?>
<!DOCTYPE html>
<html>
	<head>
        <meta charset="utf-8" />
		<title>CEVAC Database Management</title>
	</head>
	<body>
    <form method="post">
      <select>
        <?php echo buildings_html(); ?>
      </select>
      <select>
        <?php echo metrics_html(); ?>
      </select>
      <input type="submit">
    </form>
	</body>
</html>
