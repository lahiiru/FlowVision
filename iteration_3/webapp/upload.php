Select a file to upload: <br />
            <form action="upload.php" method="post" enctype="multipart/form-data">
            <input type="file" name="file" size="50" />
            <br />
            <input type="submit" value="Upload File" />
            </form>

***upload.php***

<?php
if( $_FILES['file']['name'] != "" )
{
	$destFile = "/root/mysite/upload_files/".$_FILES['file']['name'];
	move_uploaded_file( $_FILES['file']['tmp_name'], $destFile );
}
else
{
    die("No file specified!");
}
?>
<html>
<head>
<title>Uploading Complete</title>
</head>
<body>
<h2>Uploaded File Info:</h2>
<ul>
<li>Sent file: <?php echo $_FILES['file']['name'];  ?>
<li>File size: <?php echo $_FILES['file']['size'];  ?> bytes
<li>File type: <?php echo $_FILES['file']['type'];  ?>
</ul>
</body>
</html>