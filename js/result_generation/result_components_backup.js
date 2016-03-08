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

Result.prototype.getPathInfoByInputIndex = function (input) {

	/**
		returns the equivalent information for a given input index in the levenshtein path
	**/

	var lev = this.levenshtein, out = [];
	for (var step = 0; step < lev.length; step++) {
		var path_pos = lev[step];
		if (path_pos[2][1] === input) {
			out.push(path_pos[2]);
		}
	}
	return out;
};

Result.prototype.styleSingleLetterWithLevenshtein = function (input_index) {

	/*
		Creates a container with the info about the mistake at a given input position
	 */

	console.log("INPUT INDEX: ", input_index);

	var concerned_inputs = this.getPathInfoByInputIndex(input_index);
	var list_of_containers = [];

	console.log("CONCERNED INPUTS: ", concerned_inputs);

	for (var single_input in concerned_inputs) {

		var char_info = concerned_inputs[single_input];
		var input_pos = input_index;
		var target_pos = char_info[0];
		var errortype = char_info[3];

		console.log("CHARINFO: ", char_info);

		var container = $("<div>");
		container.addClass("error-container");

		var input = $("<span>");
		input.addClass("input").html("&nbsp");

		var target = $("<span>");
		target.addClass("target").html("&nbsp");

		var add_space_necessary = false;

		// console.log(input_pos + "|" + this.input[input_pos]);

		if (errortype === "M") {
			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "M+") {
			add_space_necessary = true;
			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "+M") {
			var add_space = $("<div>").addClass("error-container").html("&nbsp");
			list_of_containers.push(add_space);

			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "I") {
			input.addClass("insertion")
				.html("_");
			target.addClass("insertion")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "D") {
			input.addClass("deletion")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("deletion")
				.html("&nbsp;");
		} else if (errortype === "S") {
			input.addClass("substitution")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("substitution")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "capitalization") {
			input.addClass("capitalization")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("capitalization")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "switch") {
			input.addClass("switch")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("switch")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "punctuation") {
			input.addClass("punctuation")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("punctuation")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		}

		container.append(input);
		if (errortype !== "M" && errortype !== "D" && errortype !== "M+" && errortype !== "+M") {
			var arrow = $("<i>").addClass("fa fa-long-arrow-down arrow");
			container.append(arrow);
		}

		container.append(target);

		list_of_containers.push(container);

		if (add_space_necessary) {
			var add_space = $("<div>").addClass("error-container").html("&nbsp");
			list_of_containers.push(add_space);
		}
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

Result.prototype.createLevenshteinDiffInfo = function (target_id) {

	/*
		creates an untokenized char-by-char visual representation of the levenshtein path
	*/

	var lev = this.levenshtein;

	var parent = $(target_id);

	for (var step = 0; step < lev.length; step++){
		var position = lev[step][2];
		var input_pos = position[1];
		var target_pos = position[0];
		var errortype = position[3];

		var container = $("<div>");
		container.addClass("error-container");

		var input = $("<span>");
		input.addClass("input").html("&nbsp");

		var target = $("<span>");
		target.addClass("target").html("&nbsp");

		var add_space_necessary = false;

		// console.log(input_pos + "|" + this.input[input_pos]);

		if (errortype === "M") {
			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "M+") {
			add_space_necessary = true;
			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "+M") {
			var add_space = $("<div>").addClass("error-container").html("&nbsp");
			parent.append(add_space);

			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "I") {
			input.addClass("insertion")
				.html("_");
			target.addClass("insertion")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "D") {
			input.addClass("deletion")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("deletion")
				.html("&nbsp;");
		} else if (errortype === "S") {
			input.addClass("substitution")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("substitution")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "capitalization") {
			input.addClass("capitalization")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("capitalization")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "switch") {
			input.addClass("switch")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("switch")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "punctuation") {
			input.addClass("punctuation")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("punctuation")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
		}

		container.append(input);
		if (errortype !== "M" && errortype !== "D" && errortype !== "M+" && errortype !== "+M") {
			var arrow = $("<i>").addClass("fa fa-long-arrow-down arrow");
			container.append(arrow);
		}
		container.append(target);

		parent.append(container);
		if (add_space_necessary) {
			var add_space = $("<div>").addClass("error-container").html("&nbsp");
			parent.append(add_space);
		}

	}

};

Result.prototype.createAlignmentInfo = function (target_id) {

	/*
		Creates Alignment Info based on Map
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
		TODO
		Calcs and displays Info about distribution of Error Type
	 */

	 if (!type) {
		 type = "bar";
	 }

	var all_errors = this.levenshtein.map( function (curr) {
		return curr[2][3];
	});

	var errorCountMap = countArrayDuplicates(all_errors);
	// delete errorCountMap.M;

	// chart data and options
	var data = {
  		labels: [],
  		series: []
	};

	var pie_options = {
	    showLabel: false
	};

	var bar_options = {
		distributeSeries: true,
	};

	// map with errorshortcut mapping to className and label
	var error_type_map = {
		"M": ["error-distr-match", "correct"],
		"D": ["error-distr-deletion", "waste"],
		"I": ["error-distr-insert", "missing"],
		"S": ["error-distr-sub", "wrong"],
		"switch": ["error-distr-switch", "switched"],
		"capitals": ["error-distr-capitalization", "capitalization"],
		"punctuation": ["error-distr-punctuation", "punctuation"]
	};

	// fill data
	var char_count = this.levenshtein.length;
	for (var error in errorCountMap) {
		data["labels"].push(error_type_map[error][1]);
		data["series"].push({
			value: (errorCountMap[error] / char_count) * 100,
			className: error_type_map[error][0]
		});
	}

	console.log(data);

	//create chart
	if (type === "pie") {
		new Chartist.Pie(target_id, data, pie_options);
	} else if (type === "bar") {
		new Chartist.Bar(target_id, data, bar_options);
	}

};

Result.prototype.createPerformanceOverTimeInfo = function (target_id) {

	/*
		Show Performance over time by relating the amount of overall error to the position in text wordwise
	 */

	var words = this.word_alignment;

	var data = {
		labels: [],
		series: [[]]
	};

	var options = {
		showPoint: false,
		fullWidth: true,
		lineSmooth: Chartist.Interpolation.simple(),
		axisX: {
			showLabel: false
		},
		chartPadding: {
		    top: 15,
		    right: 0,
		    bottom: 5,
		    left: 0
		},
	};

	// fill data
	var c = 0;
	var error = 0;
	for (var index in words) {
		console.log(c, error);
		data["labels"].push(c);
		data["series"][0].push(c / (error || 1));

		c++;
		error += words[index][5];
	}

	// last part of data
	data["labels"].push(c);
	data["series"][0].push(c / (error || 1));

	console.log(data);

	// create chart
	new Chartist.Line(target_id, data, options);

};

Result.prototype.createWordwiseErrorInfo = function (target_id) {
	/*
		Shows information about each wrong word
	 */

	var words = this.word_alignment;

	for (var word in words) {
		var word_info = words[word];
		var input_word = word_info[2];
		var target_word = word_info[1];
		var word_error = word_info[5];

		// only if error occures
		if (word_error > 0 && input_word !== "") {

			//container
			var info_row = $("<div>").addClass('row');

			//content
			var info_word = $("<div>").addClass('col-xs-3');
			var info_pointer = $("<div>").addClass('col-xs-2');
 			var info_spelling = $("<div>").addClass('col-xs-7 error-indication');

			//fill content
			info_word.html(input_word);
			info_pointer.html("-->");
			for (var char = 0; char <= input_word.length; char++) {
				console.log("-----\nWORD: ", word, " CHAR: ", char);
				var containers = this.styleSingleLetterWithLevenshtein(parseInt(word_info[3]) + char);
				console.log("CONTAINERS: ", containers);
					info_spelling.append(containers[c]);
				}
			}

			// sticking stuff together
			info_row
				.append(info_word)
				.append(info_pointer)
				.append(info_spelling);

			$(target_id).append(info_row);
		}
	}


};

Result.prototype.createOverallScoreInfo = function (target_id) {

	/*
		Calcs and creates Info about Score
	*/

	// FRONTEND MATH
	var total_cost = this.levenshtein[this.levenshtein.length-1][2][2];
	var total_chars = this.levenshtein.length;

	var total_errors = 0;
	for (var i = 0; i < total_chars; i++) {if (this.levenshtein[i][2][3] !== "M") {total_errors++;} }

	var score = Math.round(total_chars / total_cost * 100)/100;

	// BACKEND MATH
	var score = this.score[0];
	var correct_words = this.score[1];
	var total_words = this.score[2];

	// DISPLAYING
	var parent = $(target_id);

	var ratio_display = $(target_id+" .ratio").html(correct_words + "/" + total_words);
	var score_display = $(target_id+" .score").html("0");
	console.log("-------------------SCORE--------------------: "score);

	var time = 100;
	function add() {
		if (cur_score < score) {
			if (cur_score >= 100 && score === Infinity) {
				score_display.html(score);
				clearInterval(score_int);
			} else {
				cur_score += 0.1;
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

	var color_ratio = total_errors / total_chars;
	if (color_ratio >= 0.8) {
		ratio_display.css("color", "red");
	} else if (color_ratio >= 0.5) {
		ratio_display.css("color", "orange");
	} else if (color_ratio >= 0.3) {
		ratio_display.css("color", "palegreen");
	} else if (color_ratio >= 0.1) {
		ratio_display.css("color", "green");
	}

	//parent.append(ratio_display).append(score_display);

};
