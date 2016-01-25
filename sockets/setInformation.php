<?php
require_once "../inc/UserSystem.php";
require_once "../inc/ErrorHandler.php";
$usersystem = new UserSystem();
$errorsystem = new ErrorHandler("setInformation");
if (isset($_POST["information"])){
    $allow = "username, age, gender, mothertongue, learninglength, livingingerman";
    $allowArr = explode(",",str_replace(" ", "", $allow));
    $infArr = json_decode($_POST["information"],true);
    if (!$infArr)
        die($errorsystem->createErrorJSON("b_setInfo_jsonparseerror"));
    foreach ($infArr as $key => $val){
        if (in_array($key, $allowArr))
           $usersystem->setUserInformation ($key, $val);
    }
    echo "OK";
} else die($errorsystem->createErrorJSON("b_setInfo_jsonparseerror"));