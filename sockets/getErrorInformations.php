<?php

/**
 * Builds up an ErrorHandler to translate JS Error Codes to actual error information arrays
 */


require_once __DIR__."/../inc/ErrorHandler.php";
header('Content-Type: application/json');

//get data from AJAX POST
$error_code = $_POST["id"];
$add_info = $_POST["add_info"];

//echo json_encode(array("name" => $error_code, "msg" => $add_info, "fatality" => "DEBUG", "debug" => " test")); die();

//create ErrorHandler
$jsErrorHandler = new ErrorHandler("FRONTEND");

//create the info
$info = $jsErrorHandler->createErrorJSON($error_code, $add_info);

echo $info;

 ?>
