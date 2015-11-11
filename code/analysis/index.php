<?php
require_once __DIR__."/../inc/config.php";
header('Content-Type: application/json');
if (empty($_POST["data"]))
    die("no data"); //todo handle error -> no data, should return a json error object
$data = json_decode($_POST["data"], true);
if ($data === null)
    die("no json"); //todo handle error -> unreadable json, should return a json error object
$new_json = array(
    "data"=>$data, 
    "session"=>array(
        //todo: add serverside information
    )
);
if (DIRECTORY_SEPARATOR == '\\' && $GLOBALS["conf"]["testing_on_windows"]){
    function shitty_escapeshellarg($st){
        return '"'.str_replace('"','\\"',$st).'"';
    }
$argument = shitty_escapeshellarg(json_encode($new_json));
} else {
$argument = escapeshellarg(json_encode($new_json));    
}
$command = __DIR__."/tgd.py $argument";

system($command); 
