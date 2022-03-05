<?php include_once("home.html");

$dirname = "./saved-images/";
$images = glob($dirname."*.jpg");

foreach($images as $image) {
    echo '<img src="'.$image.'" /><br />';
}
?>