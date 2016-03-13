<?php

require_once "../inc/UserSystem.php";
require_once "../inc/ErrorHandler.php";
require_once "../inc/SqlConnector.php";
$usersystem = new UserSystem();
$db = new SqlConnector();
$errorsystem = new ErrorHandler("submitSurvey");

$allowed = array("getstarted-rating",
                 "dictation-rating",
                 "dictation-suggestions",
                 "background-rating",
                 "wouldyouuse-rating",
                 "wouldyouuse-suggestions",
                 "learninggame-rating",
                 "learninggame-suggestions",
                 "further-suggestions");

$username = $usersystem->getUserInformation("username");
$setter = array();
if ($username)
    $setter[] = "`username` = '".$db->esc($username)."'";
foreach ($allowed as $key){
    if (!empty($_POST[$key]))
       $setter[] = "`$key` = '".$db->esc($_POST[$key])."'";
}

if (count($setter))
    $db->query($sql = "INSERT INTO survey SET ".implode(", ",$setter));

header("Location: ".strtok("http://$_SERVER[HTTP_HOST]",'?'));
die();