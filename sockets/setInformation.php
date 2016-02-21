<?php
require_once "../inc/UserSystem.php";
require_once "../inc/ErrorHandler.php";
$usersystem = new UserSystem();
$errorsystem = new ErrorHandler("setInformation");
if (isset($_POST["information"])){
    $allowArr = UserSystem::$allowed;
    $infArr = json_decode($_POST["information"],true);
    $user = !empty($_POST["username"]) ? $_POST["username"] : false;
    if (is_null($infArr))
        die($errorsystem->createErrorJSON("b_setInfo_jsonparseerror"));
    if ($user)
        $usersystem->setUser($user);
    foreach ($infArr as $key => $val){
        if (in_array($key, $allowArr))
           $usersystem->setUserInformation($key, $val);
    }
    echo json_encode($usersystem->getUserInformation(),15);

} else die($errorsystem->createErrorJSON("b_setInfo_jsonparseerror"));