$(document).ready(function() {
	$("#feedback-form").submit(function(event) {
		event.preventDefault();

		var title = $("#feedback-title").val();
		var subject = $("#feedback-subject").val();
		var message = $("#feedback-message").val();

		if (!title | !subject | !message) {
			requestErrorInfo("f_fill_all_fields", 3);
		} else {
			$.ajax({
				url: "sockets/feedback.php",
				type: 'POST',
				data: {"title": title, "subject": subject, "message": message}
			})
			.done(function() {
				console.log("success");
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
		}
	});

});
