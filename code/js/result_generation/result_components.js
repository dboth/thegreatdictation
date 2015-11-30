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

// HELPERS
Result.prototype.convertStringToPositionMap = function (str) {
	/**
		returns 	--> 	[ WORD, START, END, ERROR (default 0) ]
	**/

	var letters = str.split("");
	var pos_map = [];

	var cur_word = "", start_index = 0, cur_end_pos = 0;
	for (var i = 0; i < letters.length; i++) {
		if (letters[i] === " " || letters[i] === "\n" || i+1 === letters.length) {
			pos_map.push([cur_word, start_index, cur_end_pos-1, 0]);
			cur_word = "";
			start_index = i+1;
			cur_end_pos = start_index;
		} else if ( [".",",","!","?"].indexOf(letters[i]) >= 0 ) {
			pos_map.push([letters[i], i, i, 0]);
		} else {
			cur_word += letters[i];
			cur_end_pos += 1;
		}
	}

	return pos_map.sort(function(a, b) {
		return a[1]-b[1]; // SORTS by words starting index
	});
};

// PRODUCERS
Result.prototype.createHeader = function () {
	//Creates the header information of a result
	var header = $("#analysis-container .page-header");
    var text_id = $("<small>");
    text_id.html("<br>For Text " + this.text_id); //actually want to look up real name from DB
    header.find("h3").append(text_id);
};

Result.prototype.createSimpleDiffInfo = function () {
	// INPUT
    var input_data_html = this.input.replace(/\n/g, "").split(" ");

    var marked_input = ""; //stores the entered text labeled with wrong/correct/unknown
    for (word = 0; word < input_data_html.length; word++) {
        if (this.diff_map[word] === false) {
            marked_input += "<span class='spelling highlight wrong'>" + input_data_html[word] + "</span> ";
        } else if (this.diff_map[word] === true) {
            marked_input += "<span class='spelling highlight correct'>" + input_data_html[word] + "</span> ";
        } else {
            marked_input += "<span class='spelling highlight unlabeled'>" + input_data_html[word] + "</span> ";
        }
    }

	// TARGET
    var target_data_html = this.target.replace(/\n/g, "<br>");

	return [marked_input, target_data_html];
};

/*
	LEVENSHTEIN FUNCTIONS
*/

Result.prototype.calcLevenshteinWordErrors = function () {

	// WORD , START, END, ERROR
	var word_bag = this.convertStringToPositionMap(this.input);


	for (var step = 0; step < this.levenshtein.length; step++) {
		var cur_step = this.levenshtein[step];
		for (var word = 0; word < word_bag.length; word++) {
			var cur_word = word_bag[word];

			if (cur_word[1] <= cur_step[2][0] && cur_word[2] >= cur_step[2][0]) { // is this error in that word?

				var last_cost = 0;
				if (step !== 0) {
					last_cost = this.levenshtein[step-1][2][2];
				}

				word_bag[word][3] += cur_step[2][2] - last_cost; // add diff of cost at pos to get error cost
				break;
			}
		}
	}

	return word_bag;
};

Result.prototype.createLevenshteinDiffInfo = function (target_id) {
	// TARGET ID OF FORM "#id"
	var words = this.calcLevenshteinWordErrors();
	console.log(words);
	for (var w = 0; w < words.length; w++) {
		if (words[w][3] > 0) {
			word_box = $("<span>");
			word_box.addClass("spelling wrong");
			word_box.html(words[w][0]);
			$(target_id).append(word_box);
			word_box.css("background-color", tinycolor(word_box.css("background-color")).brighten(50-words[w][3]*10).toString() );
		} else {
			word_box = $("<span>").addClass("spelling correct");
			word_box.html(words[w][0]);
			$(target_id).append(word_box);
		}
	}

};
