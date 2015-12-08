function Result (analysis) {
	// CONTAINERS
	this.data = analysis.data;
	this.meta = analysis.meta;

	// DATA
	this.text_id = this.data.text_id;
	this.input = this.data.input;
	this.target = this.data.target;

	this.diff_map = this.data.diff_map;
	this.levenshtein = this.data.levenshtein.reverse();
}

// PREPROCESSORS

Result.prototype.convertStringToPositionMap = function (str, target) {

	/**
		returns 	--> 	[ WORD, START, END, ERROR (default 0), TARGET ]
	**/

	var lev = this.levenshtein;
	var input_letters = str.split("");
	var pos_map = [];

	console.log(input_letters);

	var cur_word = "", target_word = "", start_index = 0, cur_end_pos = 0;
	for (var i = 0; i <= input_letters.length; i++) {

		if (input_letters[i] === " " || input_letters[i] === "\n" || i+1 === input_letters.length) {
			// is potential new word

			// get errortype of letter to determine if this space is an intended new word beginning
			var errortype = "ERROR";
			for(var l_i = 0; l_i < lev.length; l_i++) {
				if (lev[l_i][2][0] === i) {
					errortype = lev[l_i][2][3];
					break;
				}
			}

			if (errortype === "M") {
				// is new word

				if (i+1 === input_letters.length) { // NOT BEAUTIFUL, but cant see another solution atm
					cur_word += input_letters[i];
					cur_end_pos++;
				}

				target_word = this.target.slice(this.getTargetPathInfo(start_index)[0], this.getTargetPathInfo(cur_end_pos)[0]);
				pos_map.push([cur_word, start_index, cur_end_pos-1, 0, target_word]);
				cur_word = "";
				start_index = i+1;
				cur_end_pos = start_index;

			} else if (errortype === "D") {
				// is not meant to be new word

				cur_word += input_letters[i];
				cur_end_pos += 1;

			} else if (errortype === "I") {
				// is meant to be new word

				target_word = this.target.slice(Math.max.apply(null, this.getTargetPathInfo(start_index)),
												Math.min.apply(null, this.getTargetPathInfo(cur_end_pos)));
				console.log(target_word, cur_end_pos, this.getTargetPathInfo(cur_end_pos));
				pos_map.push([cur_word, start_index, cur_end_pos-1, 0, target_word]);

				console.log(cur_end_pos);
				target_word = this.target.slice(Math.min.apply(null, this.getTargetPathInfo(cur_end_pos))+1, // +1 da Insert vor Leerzeichen beginnt
												Math.max.apply(null, this.getTargetPathInfo(cur_end_pos)));
				console.log(target_word);
				pos_map.push([" __ ", cur_end_pos, cur_end_pos, 0, target_word]);
				cur_word = "";
				start_index = i+1;
				cur_end_pos = start_index;

			}

		} else if (i+1 === input_letters.length) {
			// is at end of input
			cur_word += input_letters[i];
			cur_end_pos++;

			target_word = this.target.slice(this.getTargetPathInfo(start_index)[0], this.getTargetPathInfo(cur_end_pos)[0]);
			pos_map.push([cur_word, start_index, cur_end_pos-1, 0, target_word]);

		} else if ( [".",",","!","?",":",";"].indexOf(input_letters[i]) >= 0 ) {
			// is Punctuation

			target_word = this.target.slice(this.getTargetPathInfo(i)[0], this.getTargetPathInfo(i+1)[0]);

			pos_map.push([input_letters[i], i, i, 0, target_word]);

		} else {
			// is Letter

			cur_word += input_letters[i];
			cur_end_pos += 1;

		}
	}
	console.log(pos_map);
	return pos_map.sort((a, b) => a[1]-b[1]); // SORTS by words starting index
};

Result.prototype.getTargetPathInfo = function (input) {

	/**
		returns the equivalent target positions for a given input position in the levenshtein path
	**/

	var lev = this.levenshtein, out = [];
	for (var step = 0; step < lev.length; step++) {
		var path_pos = lev[step];
		if (path_pos[2][0] === input) {
			out.push(path_pos[2][1]);
		}
	}
	return out;
};

Result.prototype.calcLevenshteinWordErrors = function () {

	// WORD , START, END, ERROR
	var word_bag = this.convertStringToPositionMap(this.input);


	for (var step = 0; step < this.levenshtein.length; step++) {
		var cur_step = this.levenshtein[step];
		var found = false;
		for (var word = 0; word < word_bag.length; word++) {
			var cur_word = word_bag[word];

			if (cur_word[1] <= cur_step[2][0] && cur_word[2] >= cur_step[2][0]) { // is this error in that word?

				var last_cost = 0;
				if (step !== 0) {
					last_cost = this.levenshtein[step-1][2][2];
				}

				word_bag[word][3] += cur_step[2][2] - last_cost; // add diff of cost at pos to get error cost
				found = true;
				break;
			}
		}

		if (!found && cur_step[2][3] !== "M") {

		}

	}

	return word_bag;
};


// PRODUCERS
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
		var input_pos = position[0];
		var target_pos = position[1];
		var errortype = position[3];

		var container = $("<div>");
		container.addClass("error-container");

		var input = $("<span>");
		input.addClass("input").html("&nbsp");

		var target = $("<span>");
		target.addClass("target").html("&nbsp");

		if (errortype === "M") {
			container.addClass("no-margin");
			input.addClass("match")
				.html(this.input[input_pos].replace(/\s/g, "&nbsp"));
		} else if (errortype === "M+") {
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
		if (errortype !== "M" && errortype !== "D") {
			var arrow = $("<i>").addClass("fa fa-long-arrow-down arrow");
			container.append(arrow);
		}
		container.append(target);
		parent.append(container);

	}

};

Result.prototype.createAlignmentInfo = function (target_id) {

	/*
		Creates Alignment Info based on Map
	*/

	// TARGET ID OF FORM "#id"
	var words = this.calcLevenshteinWordErrors();

	for (var w = 0; w < words.length; w++) {
		if (words[w][3] >= 1) {
			word_box = $("<span>")
				.addClass("spelling wrong")
				.html(words[w][0]);
		} else if (words[w][3] > 0) {
			word_box = $("<span>")
				.addClass("spelling minor-mistake")
				.html(words[w][0]);
		} else {
			word_box = $("<span>")
				.addClass("spelling correct")
				.html(words[w][0]);
			$(target_id).append(word_box);
		}

		$(target_id).append(word_box);
		word_box.css("background-color", tinycolor(word_box.css("background-color")).brighten(50-words[w][3]*10).toString() );
	}

};

Result.prototype.createOverallScoreInfo = function (target_id) {

	/*
		Calcs and creates Info about Score
	*/

	var parent = $(target_id);

	var total_cost = this.levenshtein[this.levenshtein.length-1][2][2];
	var total_chars = this.levenshtein.length;

	var total_errors = 0;
	for (var i = 0; i < total_chars; i++) {if (this.levenshtein[i][2][3] !== "M") {total_errors++;} }

	var score = Math.round(total_chars / total_cost * 100)/100;

	var ratio_display = $(target_id+" .ratio").html(total_chars - total_errors + "/" + total_chars);
	var score_display = $(target_id+" .score").html("0");


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
