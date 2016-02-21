$(document).ready(function() {
	$("#feedback-form").submit(function(event) {
		event.preventDefault();

		var title = $("#feedback-title").val();
		var subject = $("#feedback-subject").val();
		var message = $("#feedback-message").val();

		console.log(title, subject, message);

		if (!title | !subject | !message) {
			requestErrorInfo("f_fill_all_fields", 3);
		} else {
			$.ajax({
				url: "sockets/feedback.php",
				type: 'POST',
				data: {"title": title, "subject": subject, "message": message}
			})
			.done(function(res) {
				console.log("success", res);
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
