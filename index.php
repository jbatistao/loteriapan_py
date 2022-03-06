<?php 

// include_once("home.html");

$dirname = "./saved-images/";
$images = glob($dirname."*.jpg");

echo '<p>Imágenes</p><br />';

foreach($images as $image) {
    echo '<img src="'.$image.'" /><br />';
}
?>