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
			if (error_count_all.hasOwnProperty(error)) {
			   error_count_all[error] = parseInt(amount);
		   	} else {
			   error_count_all[error] += parseInt(amount);
		   	}
		});
	});

	$.each(error_count_all, function(index, val) {
		 prepared_data[index] = val/levenshteins.length;
	});

	console.log(prepared_data);
	return prepared_data;
};
