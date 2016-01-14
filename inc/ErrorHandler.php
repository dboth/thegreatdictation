<?php

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
			"fatality"	=>	"", // Range: INFO DEBUG FATAL
			"name"		=>	"",
			"msg"		=>	"",
			"debug"		=>	$e_id
		);

		switch ($e_id) {
			case "b_file_not_found":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "FILE NOT FOUND";
				$error_info["msg"] = "No file found at ".$add_info;
				break;

			case "b_component_not_found":
				$error_info["fatality"] = "DEBUG";
				$error_info["name"] = "COMPONENT NOT FOUND";
				$error_info["msg"] = "No component found at ".$add_info;
				break;

			case "f_analysis_create_analysis":
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "CREATE ANALYSIS FAIL";
				$error_info["msg"] = "The creation of your analysis failed due to: ".$add_info;
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
	public function createErrorJSON($e_id, $add_info) {
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
	public function log($error_id, $add_info) {
		$error_info = $this->getErrorInfo($error_id, $add_info);
		$log_msg = date('d/m/Y H:i:s')."\t".$error_info["fatality"]."\t".$this->current_class."\t".$error_info["name"]."\t".$error_info["msg"]."\n";

		$logger = fopen($this->log_file_path, "a");
		$success = fwrite($logger, $log_msg);

		if (!$success) {
			return False;
		} else {
			return True;
		}
	}

}
