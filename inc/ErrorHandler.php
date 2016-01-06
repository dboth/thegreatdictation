<?php

/**
 * ERROR HANDLER CLASS
 * -------------------
 * Meant to be loaded in any other projects PHP Class to provide
 * simple way of logging errors, informing users, ...
 *
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
			"msg"		=>	""
		);

		switch ($e_id) {
			case 1:
				$error_info["fatality"] = "FATAL";
				$error_info["name"] = "FILE NOT FOUND";
				$error_info["msg"] = "No file found at ".$add_info;
				break;

			default:
				$error_info["fatality"] = "DEBUG";
				$error_info["name"] = "UNKNOWN ERROR";
				$error_info["msg"] = "An unknown error occured. It might be labeled wrong.";
				break;
		}

		return $error_info;
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
		$log_msg = $error_info["fatality"]."\t".$error_info["name"]."\t".$error_info["msg"];

		$logger = fopen($this->log_file_path, "a");
		$success = fwrite($logger, $log_msg);

		if (!$success) {
			return False;
		} else {
			return True;
		}
	}

}

?>
