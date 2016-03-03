<?php
//this is the entrance to the page. this script is the root of the page.

//include necessary modules
require_once "inc/config.php";
require_once "inc/TemplateGenerator.php";
require_once "inc/UserSystem.php";
$usersystem = new UserSystem();
if (isset($_GET["logout"])){
    $usersystem->logout();
    header("Location: ".strtok("http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]",'?'));
    die();
}

//set base path for includes
$GLOBALS["conf"]["base_path"] = __DIR__;

//start template generator
$template = new TemplateGenerator();
$template->printPage();
