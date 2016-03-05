$(document).ready(function() {


	// LOGIN
	$("#login-form").submit(function(event) {
		event.preventDefault();

		var username = $("#login-username").val();

		if (!username) {
			requestErrorInfo("f_fill_all_fields", 1);
		} else {
			$.ajax({
				url: "sockets/setInformation.php",
				type: 'POST',
				data: {"username": username, "information": JSON.stringify({})}
			})
			.done(function(res) {
				console.log("success", res);
				// TODO inform user about success
				$("#login-modal").modal("hide");
				console.log(window.location.search);
				if (window.location.search === "?p=register") {
					window.location.href = "?p=dictation";
				}
				window.location.reload();
			})
			.fail(function(res) {
				console.log("error", res);
			})
			.always(function() {
				console.log("complete");
			});
		}
	});

	//REGISTER
	$("#register-form").submit(function(event) {
		event.preventDefault();

		var username = $("#reg-username").val();
		var age = $("#reg-age").val();
		var gender = $("#reg-gender").val();
		var mothertongue = $("#reg-mother-tongue").val();
		var learninglength = $("#reg-learninglength").val();
		var livingingerman = $("#reg-german-country").is(":checked");

		var information_array = {"age": age, "gender": gender, "mothertongue": mothertongue, "learninglength": learninglength, "livingingerman": livingingerman};

		if (!username | !gender | !learninglength | !mothertongue) {
			requestErrorInfo("f_fill_all_fields", 4);
		} else {
			$.ajax({
				url: "sockets/setInformation.php",
				type: 'POST',
				data: {"username": username, "information": JSON.stringify(information_array)}})
			.done(function(res) {
				console.log("success", res);
				// TODO inform user about success
				$("#login-modal").modal("hide");
				window.location.href = "?p=dictation";
			})
			.fail(function(res) {
				console.log("error", res);
			})
			.always(function() {
				console.log("complete");
			});
		}
	});

});
