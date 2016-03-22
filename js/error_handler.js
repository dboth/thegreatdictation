function requestErrorInfo (error_id, add_info, target_id) {

	var error_error = {
		"msg": "There has been an error reporting this error. Whoooopsi",
		"name": "ERROR ERROR (-.-)  ",
		"fatality": "INFO"
	};

	$.ajax({
		type: "POST",
		url: "sockets/getErrorInformations.php",
		data: {id: error_id, add_info: add_info}
	}).fail(function (a, b, c) {
		console.log(a);
		console.log(b);
		console.log(c);
		informUser(error_error);
	}).done(function (error_info) {
		if (typeof error_info != "object"){
			informUser(error_error, target_id);
		}

		informUser(error_info, target_id);
	});

}

function informUser (info, target_id) {

	var weight = info["fatality"];
	var name = info["name"];
	var error_msg = info["msg"];
	var debug = info["debug"];

	var error_container = $("<div>").addClass("alert error-alert");

	switch (weight) {
		case "FATAL":
			error_container.addClass("alert-danger");
			break;

		case "WARNING":
			error_container.addClass("alert-warning");
			break;

		case "DEBUG":
			error_container.addClass("alert-warning");
			break;

		case "INFO":
			error_container.addClass("alert-info");
			break;

		default:

	}

	var dismiss_button = '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';

	error_container
		.addClass("alert-dismissible")
		.html(dismiss_button + "<strong>" + name + ": </strong>" + error_msg/* + " " + debug*/);

	if (!target_id) {
		target_id = "#content .main-container";
	}

	$(target_id).append(error_container);

}
