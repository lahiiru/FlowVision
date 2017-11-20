<?php

if(isset($_POST['submit'])){
    $name = $_FILES["file"]["name"];
//$size = $_FILES['file']['size']
//$type = $_FILES['file']['type']

    $tmp_name = $_FILES['file']['tmp_name'];
    $error = $_FILES['file']['error'];

    if (isset ($name)) {
        if (!empty($name)) {

            $location = '/var/www/html/';

            if  (move_uploaded_file($tmp_name, $location.$name)){
                echo 'Uploaded';
            }

        } else {
            echo 'please choose a file';
        }
    }
}
?>

<form action="" method="POST" enctype="multipart/form-data">
    <input type="file" name="file"><br><br>
    <input type="submit" name="submit" value="Submit">
</form>