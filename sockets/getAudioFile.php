<?php

require_once __DIR__."/../inc/SqlConnector.php";

$text_id = $_POST["text_id"];

$db = new SqlConnector();
$path = $db->getAudioByText($text_id);

echo $path;

?>
