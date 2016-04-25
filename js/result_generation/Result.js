function Result (analysis) {
	// CONTAINERS
	this.data = analysis.data;
	this.meta = analysis.meta;

	// DATA
	this.text_id = this.data.text_id;
	this.input = this.data.input;
	this.target = this.data.target;

	this.diff_map = this.data.diff_map;
	this.levenshtein = this.data.levenshtein;
	this.word_alignment = this.data.word_alignment;
	this.score = this.data.score;
}

// PREPROCESSORS

Result.prototype.getPathInfoByInputIndex = function (index) {

	/**
		returns the equivalent information for a given input index in the levenshtein path
	**/

	var lev = this.levenshtein, out = [];
	for (var step = 0; step < lev.length; step++) {
		var path_pos = lev[step];
		if (path_pos[2][1] === index) {
			out.push(path_pos[2]);
		}
	}
	return out;
};

Result.prototype.getPathInfoByTargetIndex = function (index) {

	/**
		returns the equivalent information for a given target index in the levenshtein path
	**/

	var lev = this.levenshtein, out = [];
	for (var step = 0; step < lev.length; step++) {
		var path_pos = lev[step];
		if (path_pos[2][0] === index) {
			out.push(path_pos[2]);
		}
	}
	return out;
};

Result.prototype.styleSingleLetterWithLevenshtein = function (target_index) {

	/*
		Creates a container with the info about the mistake at a given input position
	 */

	var concerned_inputs = this.getPathInfoByTargetIndex(target_index);
	var list_of_containers = [];

	for (var single_input in concerned_inputs) {

		var char_info = concerned_inputs[single_input];
		var input_pos = char_info[1];
		var target_pos = char_info[0];
		var errortype = char_info[3];

		var container = $("<div>");
		container.addClass("error-container");

		var input = $("<span>");
		input.addClass("input").html("&nbsp");

		var target = $("<span>");
		target.addClass("target");

		if (errortype === "M") {
			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "I") {
			input.addClass("insertion")
				.html("_");
			target.addClass("insertion")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "D") {
			container.addClass('no-margin');
			input.addClass("deletion")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "S") {
			input.addClass("substitution")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("substitution")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "capitals" || errortype === "caveat_capitalization") {
			input.addClass("capitalization")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("capitalization")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "switch") {
			input.addClass("switch")
				.html((this.input[input_pos] + this.target[target_pos]).replace(/\s/g, "&nbsp"));
			target.addClass("switch")
				.html("<i class='fa fa-exchange'></i>");
		} else if (errortype === "punctuation" || errortype === "punctfault_t" || errortype === "sim_punct") {
			console.log("LENGTH: " + this.input.length + "; POS: " + input_pos);
			input.addClass("punctuation")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("punctuation")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "punctfault_i") {
			console.log("LENGTH: " + this.input.length + "; POS: " + input_pos);
			input.addClass("punctuation")
				.html("_");
			target.addClass("punctuation")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		}

		container.append(input);
		if (target.html()) {
			container.append(target);
		}

		list_of_containers.push(container);
	}

	return list_of_containers;
};

// CREATIONS

Result.prototype.createHeader = function (target_id) {

	/*
		Creates the header information of a result
	*/

	var header = $(target_id);
    var text_id = $("<small>");
    text_id.html("<br>For Text " + this.text_id); //actually want to look up real name from DB
    header.find("h3").append(text_id);
};

Result.prototype.createWordwiseErrorInfo = function (target_id) {

	/*
		Creates Word Alignment Info about wordwise Errors based on Map
	*/


	var words = this.word_alignment;

	for (var input_start in words) {

		var word_info = words[input_start];
		var input_word = word_info[2];
		var target_word = word_info[1];
		var word_error = word_info[5];

		var container = $("<div>").addClass('alignment-word-container');
		var word_box = $("<div>");

		if (input_word === "") {
			word_box
				.addClass("spelling missing-word")
				.html(target_word);
		} else if (word_error >= 3) {
			word_box
				.addClass("spelling wrong")
				.html(input_word);
		} else if (word_error > 0) {
			word_box
				.addClass("spelling minor-mistake")
				.html(input_word);
		} else {
			word_box
				.addClass("spelling correct")
				.html(input_word);
			$(target_id).append(word_box);
		}

		container.append(word_box);

		// add info about correct spelling
		if (!word_box.hasClass('correct') && !word_box.hasClass('missing-word')) {
			correct_spelling_info = $("<div>")
				.addClass('correct-spelling-info')
				.html(target_word);
			container.append(correct_spelling_info);
		}

		// add word to container
		$(target_id).append(container);

		//word_box.css("background-color", tinycolor(word_box.css("background-color")).brighten(50-word_error*10).toString() );

	}

};

Result.prototype.createMistakeDistributionInfo = function (target_id, type) {

	/*
		Calcs and displays Info about distribution of Error Type
	 */

	if (!type) {
		type = "bar";
	}

	var target_div = $(target_id);

	/* PREPARE CHART */
	var canvas = $("<canvas>").attr({
		width: target_div.width(),
		height: (type === "bar") ? 200 : 400
	});
	var context = canvas.get(0).getContext("2d");

	var data = {
  		labels: [],
  		datasets: [
			{
				label: "Error Type Distribution",
	            data: []
			}
		]
	};

	if (type === "bar") {

		data["datasets"][0].fillColor = "blue";
		data["datasets"][0].strokeColor = "lightblue";
		data["datasets"][0].highlightFill = "green";
		data["datasets"][0].highlightStroke = "lightgreen";

	} else if (type === "radar") {

		data["datasets"][0].fillColor = "rgba(151,187,205,0.2)";
		data["datasets"][0].fillColor = "rgba(151,187,205,0.2)";
        data["datasets"][0].strokeColor = "rgba(151,187,205,1)";
        data["datasets"][0].pointColor = "rgba(151,187,205,1)";
        data["datasets"][0].pointStrokeColor = "#fff";
        data["datasets"][0].pointHighlightFill = "#fff";
        data["datasets"][0].pointHighlightStroke = "rgba(151,187,205,1)";

	} else if (type === "pie") {

		// TODO

	}

	/* PREPARE DATA */

	var all_errors = this.levenshtein.map( function (curr) {
		return curr[2][3];
	});

	var error_count_map = countArrayDuplicates(all_errors);
	console.log(error_count_map);
	delete error_count_map["M"];
	delete error_count_map["M+"];
	delete error_count_map["+M"];

	// map with errorshortcut mapping to className and label
	var error_type_map = {
		"M": "correct",
		"D": "waste",
		"I": "missing",
		"S": "wrong",
		"switch": "switched",

		"capitals": "capitalization",
		"caveat_capitalization": "capitalization",

		"punct": "punctuation",
		"punctfault_t": "punctuation",
		"punctfault_i": "punctuation",
		"sim_punct": "similar punctuation",

		"word_switch": "word switch"
	};

	var color_map = {
		correct: "match",
		waste: "deletion",
		missing: "insertion",
		wrong: "substitution",
		switched: "switch",
		capitalization: "capitalization",
		punctuation: "punctuation",
		"word switch": "word-switch"
	};

	/* FILL DATA */

	// get total amount of wrong chars for percentage
	var char_count = 0;
	for (var el in error_count_map) {
		char_count += error_count_map[el];
	}

	for (var error in error_count_map) {
		// catch unknown error types, shouldnt happen tho
		var error_label = "unknown";

		if (error_type_map[error]) {
			error_label = error_type_map[error];
		}

		var label_pos = data["labels"].indexOf(error_label);
		console.log(error_label + " -> " + label_pos);
		if (label_pos === -1) {
			// write into data object
			data["labels"].push(error_label);
			data["datasets"][0]["data"].push((type === "pie") ? ((error_count_map[error] / char_count) * 100) : error_count_map[error]);
		} else {
			// add to already existing label
			data["datasets"][0]["data"][label_pos] += (type === "pie") ? ((error_count_map[error] / char_count) * 100) : error_count_map[error];
		}
	}

	/* CREATE CHART */
	target_div.append(canvas);

	if (type === "radar") {
		var radar_chart = new Chart(context).Radar(data, {
			responsive: true
		});

		return radar_chart;

	} else if (type === "bar") {
		var bar_chart = new Chart(context).Bar(data, {
			responsive: true
		});

		for (var index in data["labels"]) {
			if (data["labels"].hasOwnProperty(index)) {
				var label_color = $(".element." + color_map[data["labels"][index]]).css("background-color");
				bar_chart.datasets[0].bars[index].fillColor = label_color;
				bar_chart.datasets[0].bars[index].strokeColor = tinycolor(label_color).lighten(10);
				bar_chart.datasets[0].bars[index].highlightFill = tinycolor(label_color).lighten(15);
				bar_chart.datasets[0].bars[index].highlightStroke = tinycolor(label_color).lighten(20);
			}
		}

		bar_chart.update();

		return bar_chart;
	}

};

Result.prototype.createPerformanceOverTimeInfo = function (target_id) {

	/*
		Show Performance over time by relating the amount of overall error to the position in text wordwise
	 */

	var target_div = $(target_id);

	/* PREPARE CHART */
 	var canvas = $("<canvas>").attr({
 		width: target_div.width(),
 		height: 200
 	});
 	var context = canvas.get(0).getContext("2d");

 	var data = {
   		labels: [],
   		datasets: [
 			{
 				label: "Error Type Distribution",
	            fillColor: "rgba(151,187,205,0.2)",
	            strokeColor: "rgba(151,187,205,1)",
	            pointColor: "rgba(151,187,205,1)",
	            pointStrokeColor: "#fff",
	            pointHighlightFill: "#fff",
	            pointHighlightStroke: "rgba(151,187,205,1)",
 	            data: []
 			}
 		]
 	};


	var words = this.word_alignment;

	/* FILL DATA */
	var c = 0;
	var error = 0;
	for (var index in words) {
		data["labels"].push(c);
		data["datasets"][0]["data"].push(c / (error || 1));

		c++;
		error += words[index][5];
	}

	// last part of data
	data["labels"].push(c);
	data["datasets"][0]["data"].push(c / (error || 1));

	// create chart
	target_div.append(canvas);
	var line_chart = new Chart(context).Line(data, {
		responsive: true,
		pointHitDetectionRadius : 3,
		pointDot: false
	});

};

Result.prototype.createCharwiseErrorInfo = function (target_id) {
	/*
		Shows charwise information about each wrong word
	 */

	var words = this.word_alignment;

	for (var word in words) {
		var word_info = words[word];

		var input_word = word_info[2];
		var input_start = word_info[3];
		var input_end = word_info[4];

		var target_word = word_info[1];
		var target_start = word;
		var target_end = word_info[0];

		var word_error = word_info[5];

		// only if error occures
		if (word_error > 0 && input_word !== "" && word_info[6] === null) {

			//container
			var info_row = $("<div>").addClass('dictation-spelling-row');

			//content
			var info_target_word = $("<div>");
			var info_input_word = $("<div>");
 			var info_spelling = $("<div>").addClass('charwise-word-wrapper');

			//fill content
			info_target_word.html(target_word);
			info_input_word.html(input_word);

			// Basis has to be target, because on one target character there can be multiple linked input positions
			for (var char = target_start-1; char <= target_end; char++) {
				var containers = this.styleSingleLetterWithLevenshtein(char);
				for (var c in containers) {
					info_spelling.append(containers[c]);
				}
			}

			// sticking stuff together
			info_row
				.append(info_input_word)
				.append(info_spelling);

			$(target_id).append(info_row);
		}
	}


};

Result.prototype.createOverallScoreInfo = function (target_id) {

	/*
		Calcs and creates Info about Score
	*/

	// BACKEND MATH
	var score = this.score[0];
	var correct_words = this.score[1];
	var total_words = this.score[2];

	// DISPLAYING
	var parent = $(target_id);

	var ratio_display = $(target_id+" .ratio").html(correct_words + "/" + total_words);
	var score_display = $(target_id+" .score").html("0");

	var time = 100;
	function add() {
		if (cur_score < score) {
			if (cur_score >= 100 && score === "Infinity") {
				score_display.html(score);
				clearInterval(score_int);
			} else {
				cur_score += 0.1;
				cur_score = Math.round(cur_score *10)/10;
				score_display.html(Math.round(cur_score*100)/100);
				clearInterval(score_int);
				time--;
				score_int = setInterval(add, time);
			}
		} else {
			clearInterval(score_int);
		}
	}

	var cur_score = 0;
	var score_int = setInterval(add, time);

	//parent.append(ratio_display).append(score_display);

};
