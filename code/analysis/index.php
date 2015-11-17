<?php
//include the configs
require_once __DIR__."/../inc/config.php";

//set the output to json
header('Content-Type: application/json');



//check if there was data sent
if (empty($_POST["data"]))
    die("no data"); //todo handle error -> no data, should return a json error object



//try to decode the data. data must be in json
$data = json_decode($_POST["data"], true);

//check if data is json
if ($data === null)
    die("no json"); //todo handle error -> unreadable json, should return a json error object

//create a new data object with meta data
$new_json = array(
    "data"=>$data, 
    "meta"=>array(
        //todo: add serverside information
    )
);

//escapeshellarg is shitty for windows because it replaces all double quotes.
//therefore if on windows and testing do not use that and escape the argument with a rudimentary version of the escaper
if (DIRECTORY_SEPARATOR == '\\' && $GLOBALS["conf"]["testing"]){
    //the rudimentary escaper
    function shitty_escapeshellarg($st){
        return '"'.str_replace('"','\\"',$st).'"';
    }
    $argument = shitty_escapeshellarg(json_encode($new_json));
} else {
    //on linux everythings fine
    $argument = escapeshellarg(json_encode($new_json));    
}

//var_dump($argument);

//create the command
$command = "python ". __DIR__ ."/tgd.py $argument";

//execute the command (system() prints the output)
system($command); 