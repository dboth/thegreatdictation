$(document).ready(function() {

	function displayStatistics(username, limit, offset) {
		$.ajax({
			url: 'sockets/getDictationsForUser.php',
			type: 'POST',
			data: {
				"username": username,
				"limit": limit,
				"offset": offset
			}
		})
		.done(function(dictations) {
			//console.log(dictations);
			dictations = JSON.parse(dictations);

			var statistics_object = new Statistics(dictations);

			statistics_object.prepareDataForAvgErrorDistribution();

		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	}

	$.ajax({
		url: 'sockets/setInformation.php',
		type: 'POST',
		data: {username: '', information: "{}"}
	})
	.done(function(res) {
		console.log("success");
		res = JSON.parse(res);
		var user = res["username"];

		displayStatistics(user, 50, 0);
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});

});
