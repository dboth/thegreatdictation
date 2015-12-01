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
	console.log(this.levenshtein);
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
												Math.max.apply(null, this.getTargetPathInfo(cur_end_pos-1)));
				console.log(target_word, cur_end_pos, this.getTargetPathInfo(cur_end_pos));
				pos_map.push([cur_word, start_index, cur_end_pos-1, 0, target_word]);

				target_word = this.target.slice(this.getTargetPathInfo(cur_end_pos+1)+1, this.getTargetPathInfo(cur_end_pos+2));
				console.log(target_word);
				pos_map.push([" __ ", cur_end_pos, cur_end_pos, 0, target_word]);
				cur_word = "";
				start_index = i+1;
				cur_end_pos = start_index;

			}

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
Result.prototype.createHeader = function () {
	//Creates the header information of a result
	var header = $("#analysis-container .page-header");
    var text_id = $("<small>");
    text_id.html("<br>For Text " + this.text_id); //actually want to look up real name from DB
    header.find("h3").append(text_id);
};

Result.prototype.createLevenshteinDiffInfo = function (target_id) {
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
