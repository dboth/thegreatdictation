function createAnalysis(dict_res, all_res) {

    /*
     * Function to use results of analysis and build up an evaluation page
     * for the user.
     */

    console.log("ALL: ", all_res);
    var result_object = new Result(dict_res);
    var avg_object = new Statistics(all_res);
    var avg_error_distr = avg_object.prepareDataForAvgErrorDistribution();

    result_object.createWordwiseErrorInfo("#input-info-container");

    result_object.createOverallScoreInfo("#score-info");

    result_object.createPerformanceOverTimeInfo("#performance-over-time-chart");
    result_object.createCharwiseErrorInfo("#wordwise-error-info");

    var distr_chart_radar = result_object.createMistakeDistributionInfo("#error-distribution-chart-radar", "radar", avg_error_distr);
    var distr_chart_bar = result_object.createMistakeDistributionInfo("#error-distribution-chart-bar", "bar", avg_error_distr);
    // EventHandler for Error Distribution Tabpanel, that reinitializes the charts such that they are visible. Ugly but necessary Workaround
    $(document).ready(function() {
    	$('#error-distr-radar-tab').click(function (e) {
    		e.preventDefault();
            $(this).tab('show');
            $("#error-distribution-chart-radar").find('canvas').remove();
            distr_chart_radar.destroy();
            distr_chart_radar = result_object.createMistakeDistributionInfo("#error-distribution-chart-radar", "radar", avg_error_distr);
    	});

        $('#error-distr-bar-tab').click(function (e) {
    		e.preventDefault();
            $(this).tab('show');
            distr_chart_bar.destroy();
            $("#error-distribution-chart-bar").find('canvas').remove();
            distr_chart_bar = result_object.createMistakeDistributionInfo("#error-distribution-chart-bar", "bar", avg_error_distr);
    	});
    });

}


$(document).ready(function () {
    /*

    AJAX HANDLING, FORM LISTENER
    INITITALISES WHOLE PROCESS

    */

    $.ajax({
		url: 'sockets/setInformation.php',
		type: 'POST',
		data: {username: '', information: "{}"}
	})
	.done(function(res) {
        $("#dictation-form").submit(function (event) {
            event.preventDefault();
            var audio_player = $("#audio-player");
            audio_player.trigger("pause");
            audio_player.currentTime = 0;

            var data = {
                input: $("#dictation-text").val().replace(/\s$/, ""),
                text_id: $("#dictation-id").val(),
                target: ""
            };

            var action = $(this).attr("action");
            var method = $(this).attr("method");

            toggleViews("#loading-container");
            loadingbar("#loading-bar", 2000);

            var username = JSON.parse(res)["username"];
            var limit = 50;
            var offset = 0;

            //SEND AND RECEIVE DATA FROM SERVER
            $.when(
                $.ajax({
                    url: action,
                    data: {data: JSON.stringify(data)},
                    type: method
                }),
                $.ajax({
        			url: 'sockets/getDictationsForUser.php',
        			type: 'POST',
        			data: {
        				"username": username,
        				"limit": limit,
        				"offset": offset
        			}
        		})
            ).then(function(dictation_result, all_results) {
                var loadingbar = $("#loading-bar .progress-bar");
                loadingbar.stop();
                console.log("RESULT: ", dictation_result);
                console.log("ALL DICTATIONS: ", all_results);
                loadingbar.animate({ width: "100%" }, {easing: "linear", duration: 100, complete: function () {
                    toggleViews("#analysis-container");
                    createAnalysis(dictation_result[0][0], JSON.parse(all_results[0]));
                    $("#res-switch").addClass("active");
                    $("#dict-switch").removeClass("active");
                }});
            }).fail(function (a,b,c){
                console.log("ERROR: ", a.responseText);
                requestErrorInfo("f_analysis_display_analysis", "Server Request Failed");
            });
        });
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});

});
