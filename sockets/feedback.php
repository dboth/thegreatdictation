<?php
require_once __DIR__."/../inc/config.php";
require_once __DIR__."/../inc/sqlConnector.php";

$db = new SqlConnector();
if ($db->putFeedback($title, $subject, $text))
    echo "OK";
else 
    echo "ERROR";