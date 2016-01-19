<?php

//TAKES POST REQUEST WITH PARAMS:
//title, subject, text
//AND SAVES THEM IN THE DB



require_once __DIR__."/../inc/config.php";
require_once __DIR__."/../inc/SqlConnector.php";

$title = $_POST["title"];
$subject = $_POST["subject"];
$text = $_POST["message"];

if (empty($title) || empty($subject) || empty($text))
    die($title." AND ".$subject." AND ".$text);

$db = new SqlConnector();

if (!($db->saveFeedback($title, $subject, $text)))
    die("ERROR");

die("OK");

?>
