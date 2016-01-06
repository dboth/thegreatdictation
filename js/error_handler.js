function ErrorHandler(error_id, error_info, error_loc) {
	this.error_id = error_id, // ID to identify error type
	this.error_info = error_info, // Additional Infos
	this.error_loc = error_loc // FILE where the error occured
}

ErrorHandler.prototype.createUserMessage = function () {
	var msg = "AN ERROR OCCURED (CODE: " + error_id + "): ";
	switch (this.error_id) {
		case 1:
			//FILE NOT FOUND

		default:

	}

	

	return msg;
};
