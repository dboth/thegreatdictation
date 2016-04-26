$(document).ready(function() {

	function displayDictations(username, limit, offset) {
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
			console.log(dictations);

			var target_div = $("#dictation-list");
			var row = $("<div>").addClass('row');

			for (var key in dictations) {
				if (dictations.hasOwnProperty(key)) {

					var dict = dictations[key];

					var col = $("<div>").addClass('col-xs-12 col-sm-12');
					var dor = $("<div>").addClass('dictation-overview-row');

					if (parseInt(dict["correct_words"])/parseInt(dict["total_words"]) >= 0.75) {
						dor.addClass('good');
					} else if (parseInt(dict["correct_words"])/parseInt(dict["total_words"]) <= 0.25) {
						dor.addClass('bad');
					} else {
						dor.addClass('mediocre');
					}

					var dict_name = $("<div>").addClass('dict-title').html(dict["name"]);
					var dict_corrects = $("<div>").addClass('dict-corrects').html(dict["correct_words"] + " / " + dict["total_words"]);
					var dict_score = $("<div>").addClass('dict-score').html(dict["score"]);
					var dict_id = $("<div>").attr({
						hidden: "hidden",
						class: 'dict-id'
					}).html(dict["dict_id"]);
					var dict_output = $("<div>").attr({
						hidden: "hidden",
						class: 'dict-output'
					}).html(dict["output"]);
					var chevron = '<i class="fa fa-chevron-right" aria-hidden="true"></i>';


					row.append(col);
					col.append(dor);
					dor.append(dict_name, dict_corrects, dict_score, dict_id, dict_output, chevron);

					target_div.append(row);

				}
			}

			$(".dictation-overview-row").click(function(event) {
				var id = $(this).find(".dict-id").html();
				var dict_result = JSON.parse($(this).find(".dict-output").html());
				var target = $("#dictation-showcase");
				target.html("");

				var back_button_row = $("<div>").addClass('row');
				var back_button_col = $("<div>").addClass('col-xs-12 text-center');
				var back_button = $("<button>").attr({
					type: 'button',
					class: 'btn btn-primary',
					id: "back-to-list"
				}).html("Return to your dictations");

				back_button_row.append(back_button_col);
				back_button_col.append(back_button);

				console.log("OVERVIEW ROW: ", dict_result[0], dictations);

				target.load("frontend/components/result_page.php", function(event) {
					toggleViews("#dictation-showcase");
					target.prepend(back_button_row);
					createAnalysis(dict_result[0], dictations);

					$("#back-to-list").click(function(event) {
						toggleViews("#dictation-list");
					});
				});

			});


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

		displayDictations(user, 10, 0);
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});

});
