$(document).ready(function() {

	$("#reg-username").focusout(function(event) {

		var email_notification = $("<div>").attr({
			id: 'email-validation-notification',
			class: 'validation-notification'
		});

		if (!isEmail($(this).val()) && $(this).val() !== "") {
			$('#reg-username-col').append(email_notification.html("not a valid email"));
		}
	});

	$("#reg-age").focusout(function(event) {

		var age_notification = $("<div>").attr({
			id: 'age-validation-notification',
			class: 'validation-notification'
		});

		if ($(this).val() < 14) {
			$('#reg-age-col').append(age_notification.html("you should be at least 14"));
		}
	});

	$(".register-field").focusin(function(event) {

		var notifications = $(this).children('.validation-notification');
		notifications.remove();

	});

});
