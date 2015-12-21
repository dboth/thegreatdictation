<?php
//include the configs
require_once __DIR__."/../inc/config.php";
require_once __DIR__."/../inc/sqlConnector.php";

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
$input_json = json_encode($new_json);
//escapeshellarg is shitty for windows because it replaces all double quotes.
//therefore if on windows and testing do not use that and escape the argument with a rudimentary version of the escaper
if (DIRECTORY_SEPARATOR == '\\' && $GLOBALS["conf"]["testing"]){
    //the rudimentary escaper
    function shitty_escapeshellarg($st){
        return '"'.str_replace('"','\\"',$st).'"';
    }
    $argument = shitty_escapeshellarg($input_json);
} else {
    //on linux everythings fine
    $argument = escapeshellarg($input_json);
}

//var_dump($argument);

//create the command
$command = "python ". __DIR__ ."/analyse.py $argument";

//execute the command (system() prints the output) exec does not
$output = exec($command);
/* ONLY WORKS ON SERVER..
$sql = new SqlConnector();
$sql->saveAnalysisResult($input_json, $output);
*/