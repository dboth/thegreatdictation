<?php

require_once __DIR__."/config.php";

/**
 * ERROR HANDLER CLASS
 * -------------------
 * Meant to be loaded in any other projects PHP Class to provide
 * simple way of logging errors, informing users, ...
 *
 * IMPORTANT: apache user needs full permissions to the log directory!
 */

class ErrorHandler {

	public function __construct($current_class) {
		$this->current_class = $current_class;
		$this->log_file_path = $GLOBALS["conf"]["log_path"];
	}

	/**
	 * Function gets information about an error based on ID and optional additional information
	 * @param  int		$e_id		ID of the error
	 * @param  str		$add_info 	additional info about error depending on errortype
	 * @return array           		contains fatality, name and msg for error
	 */
	protected function getErrorInfo($e_id, $add_info) {
		$error_info = array(
			"fatality"	=>	"", // Range: INFO DEBUG WARNING FATAL
			"name"		=>	"",
			"msg"		=>	"",
			"debug"		=>	$e_id
		);

		switch ($e_id) {
			case "b_missing_post_error":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "MISSING POST";
				$error_info["msg"] = "Needed data wasnt provided in POST: ".$add_info;
				break;
			case "b_info":
				$error_info["fatality"] = "INFO";
				$error_info["name"] = "NOTE";
				$error_info["msg"] = $add_info;
				break;
			case "b_file_not_found":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "FILE NOT FOUND";
				$error_info["msg"] = "No file found at ".$add_info;
				break;
            case "b_usersystem_key_not_found":
				$error_info["fatality"] = "WARNING";
				$error_info["name"] = "KEY NOT FOUND";
				$error_info["msg"] = "The following key could not be found in the user session: ".$add_info;
				break;
            case "b_setInfo_jsonparseerror":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "JSON NOT PARSEABLE";
				$error_info["msg"] = "The setInformation Socket could not parse the incoming json.";
				break;
			case "b_component_not_found":
				$error_info["fatality"] = "DEBUG";
				$error_info["name"] = "COMPONENT NOT FOUND";
				$error_info["msg"] = "No component found at ".$add_info;
				break;
           case "b_page_not_found":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "page NOT FOUND";
				$error_info["msg"] = "No page found at ".$add_info;
				break;

			// DATABASE ERRORS
            case "b_db_connection_error":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "COULDNT SQL";
				$error_info["msg"] = "Couldnt: ".$add_info;
				break;
			case "b_db_couldnt_prepare_sql":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "COULDNT PREPARE SQL";
				$error_info["msg"] = "Couldnt prepare the SQL Statement for execution at: ".$add_info;
				break;

			// FRONTEND ERRORS
			case "f_analysis_display_analysis":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "CREATE ANALYSIS FAIL";
				$error_info["msg"] = "The creation of your analysis failed due to: ".$add_info;
				break;
			case "f_fill_all_fields":
				$error_info["fatality"] = "WARNING";
				$error_info["name"] = "FILL ALL FIELDS";
				$error_info["msg"] = "Please fill all ".$add_info." required fields!";
				break;
			case "f_select_a_text":
				$error_info["fatality"] = "WARNING";
				$error_info["name"] = "SELECT A TEXT";
				$error_info["msg"] = "Please select a text!";
				break;
			case "f_user_doesnt_exist":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "USER NOT FOUND";
				$error_info["msg"] = "The username you entered doesnt exist. Please check your spelling or register first!";
				break;
			case "f_username_not_valid":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "EMAIL INVALID";
				$error_info["msg"] = "Please provide a valid email!";
				break;

			default:
				$error_info["fatality"] = "DEBUG";
				$error_info["name"] = "UNKNOWN ERROR";
				$error_info["msg"] = "An unknown error occured.".$e_id;
				break;
		}

		return $error_info;
	}

	/**
	 * Builds an Array in JSON format thats meant to be used by frontend
	 * to present the user Infos about what happened
	 * @param	int		$error_id	ID of error to be logged
	 * @param	str		$add_info	Additional Info concerning error
	 * @return 	json	           	json/arraymap containing the information for the frontend
	 */
	public function createErrorJSON($e_id, $add_info="") {
		$error_info = $this->getErrorInfo($e_id, $add_info);
		return json_encode($error_info);
	}

	/**
	 * Function logs errors to LOG FILE (defined in config)
	 *
	 * @param	int		$error_id	ID of error to be logged
	 * @param	str		$add_info	Additional Info concerning error
	 * @return	bool			True if logging succesful, False else
	 */
	public function log($error_id, $add_info="") {
		$error_info = $this->getErrorInfo($error_id, $add_info);
		$log_msg = date('d/m/Y H:i:s')."\t".$error_info["fatality"]."\t".$this->current_class."\t".$error_info["name"]."\t".$error_info["msg"]."\n";

		$logger = fopen($this->log_file_path, "a");
		$success = fwrite($logger, $log_msg);

		if (!$success) {
			return False;
		} else {
			return $this->createErrorJSON($error_id, $add_info);
		}
	}

}
