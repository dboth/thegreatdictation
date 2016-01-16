<?php

//TAKES POST REQUEST WITH PARAMS:
//title, subject, text
//AND SAVES THEM IN THE DB



require_once __DIR__."/../inc/config.php";
require_once __DIR__."/../inc/SqlConnector.php";

$title = $_POST["title"];
$subject = $_POST["subject"];
$text = $_POST["text"];

if (empty($title) || empty($subject) || empty($text)) 
    die("ERROR");

$db = new SqlConnector();

if (!$db->putFeedback($title, $subject, $text))
    die("ERROR");

die("OK");