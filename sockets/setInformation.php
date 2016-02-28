<?php

/*

this is the interface for the usersystem to javascript

takes a post request with the following parameters:
 * username: string
 * information: json object

if username is not empty the username gets set and the information for this
username in the database will be written in the session key-value storage.
All existing key-values in the session will be deleted.

if information contains elements the key will if allowed saved with its value
into the key-value storage. If a username was set before the data will also be
saved into the database.

The request returns a json object resembling the current key-value storage.
Username and information can both be empty to only receive this without any
changes.

*/

require_once "../inc/UserSystem.php";
require_once "../inc/ErrorHandler.php";
$usersystem = new UserSystem();
$errorsystem = new ErrorHandler("setInformation");

if (isset($_POST["information"])){

    $allowArr = UserSystem::$allowed;
    $infArr = json_decode($_POST["information"], true);
    $user = !empty($_POST["username"]) ? $_POST["username"] : false;

    if (is_null($infArr)) {
        die($errorsystem->createErrorJSON("b_setInfo_jsonparseerror"));
    }

    if ($user) {
        $usersystem->setUser($user);
    }

    foreach ($infArr as $key => $val){
        if (in_array($key, $allowArr)){
            
        $usersystem->setUserInformation($key, $val);}
    }

    echo json_encode($usersystem->getUserInformation(), 15);

} else {
    die($errorsystem->createErrorJSON("b_setInfo_jsonparseerror"));
}
