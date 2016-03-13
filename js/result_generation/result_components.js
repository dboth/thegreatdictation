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
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
			target.addClass("switch")
				.html(this.target[target_pos].replace(/\s/g, "&nbsp"));
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

Result.prototype.createAlignmentInfo = function (target_id) {

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
		TODO
		Calcs and displays Info about distribution of Error Type
	 */

	 if (!type) {
		 type = "bar";
	 }

	var all_errors = this.levenshtein.map( function (curr) {
		return curr[2][3];
	});

	var error_count_map = countArrayDuplicates(all_errors);
	console.log(error_count_map);
	delete error_count_map["M"];
	delete error_count_map["M+"];
	delete error_count_map["+M"];

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
		onlyInteger: true
	};

	// map with errorshortcut mapping to className and label
	var error_type_map = {
		"M": ["error-distr-match", "correct"],
		"D": ["error-distr-deletion", "waste"],
		"I": ["error-distr-insert", "missing"],
		"S": ["error-distr-sub", "wrong"],
		"switch": ["error-distr-switch", "switched"],

		"capitals": ["error-distr-capitalization", "capitalization"],
		"caveat_capitalization": ["error-distr-capitalization", "capitalization"],

		"punct": ["error-distr-punctuation", "punctuation"],
		"punctfault_t": ["error-distr-punctuation", "punctuation"],
		"punctfault_i": ["error-distr-punctuation", "punctuation"],
		"sim_punct": ["error-distr-similar-punctuation", "similar punctuation"],

		"word_switch": ["error-distr-word-switch", "word switch"] // !
	};

	// fill data
	var char_count = 0;
	for (var el in error_count_map) {
		char_count += error_count_map[el];
	}

	for (var error in error_count_map) {
		// catch unknown error types, shouldnt happen tho
		var error_label = "unknown";
		var error_css = "error-distr-unknown"

		if (error_type_map[error]) {
			error_label = error_type_map[error][1];
			error_css = error_type_map[error][0];
		}

		// write into data object
		data["labels"].push(error_label);
		data["series"].push({
			value: (type === "pie") ? ((error_count_map[error] / char_count) * 100) : error_count_map[error],
			className: error_css
		});
	}

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
		data["labels"].push(c);
		data["series"][0].push(c / (error || 1));

		c++;
		error += words[index][5];
	}

	// last part of data
	data["labels"].push(c);
	data["series"][0].push(c / (error || 1));

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
		var input_start = word_info[3];
		var input_end = word_info[4];

		var target_word = word_info[1];
		var target_start = word;
		var target_end = word_info[0];

		var word_error = word_info[5];

		// only if error occures
		if (word_error > 0 && input_word !== "") {

			//container
			var info_row = $("<div>").addClass('row row-spacing');

			//content
			var info_target_word = $("<div>").addClass('col-xs-5 col-sm-3');
			var info_input_word = $("<div>").addClass('col-sm-3 hidden-xs');
			var info_pointer = $("<div>").addClass('col-sm-2 hidden-xs');
 			var info_spelling = $("<div>").addClass('col-xs-7 col-sm-4 error-indication');

			//fill content
			info_target_word.html(target_word);
			info_input_word.html(input_word);
			info_pointer.html("");

			// Basis has to be target, because on one target character there can be multiple linked input positions
			for (var char = target_start-1; char <= target_end; char++) {
				var containers = this.styleSingleLetterWithLevenshtein(char);
				for (var c in containers) {
					info_spelling.append(containers[c]);
				}
			}

			// sticking stuff together
			info_row
				.append(info_target_word)
				.append(info_input_word)
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

	var time = 100;
	function add() {
		if (cur_score < score) {
			if (cur_score >= 100 && score === Infinity) {
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
