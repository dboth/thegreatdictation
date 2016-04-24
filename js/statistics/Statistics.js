function Statistics(dictations) {
	this.dictations = dictations;
}

Statistics.prototype.prepareDataForAvgErrorDistribution = function () {
	var prepared_data = {};
	var levenshteins = this.dictations.map(function(curr) {
		return JSON.parse(curr["output"])[0]["data"]["levenshtein"].map(function(step){
			return step[2][3];
		});
	});

	var error_count_seperate = levenshteins.map(function(curr) {
		return countArrayDuplicates(curr);
	});

	var error_count_all = {};
	$.each(error_count_seperate, function(index, dict) {
		$.each(dict, function(error, amount) {
			console.log(error, amount);
			if (!error_count_all.hasOwnProperty(error)) {
			   error_count_all[error] = parseInt(amount);
		   	} else {
			   error_count_all[error] += parseInt(amount);
		   	}
		});
		console.log(error_count_all);
	});

	$.each(error_count_all, function(index, val) {
		 prepared_data[index] = val/levenshteins.length;
	});

	return prepared_data;
};

Statistics.prototype.displayAvgErrorDistribution = function(avgdata, target_id, type) {
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

	var error_count_map = avgdata;
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
