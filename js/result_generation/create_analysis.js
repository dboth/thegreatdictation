function createAnalysis(res) {

    /*
     * Function to use results of analysis and build up an evaluation page
     * for the user.
     */

    var result_object = new Result(res[0]);

    result_object.createHeader("#analysis-container .page-header");

    result_object.createWordwiseErrorInfo("#input-info-container");

    result_object.createOverallScoreInfo("#score-info");

    result_object.createPerformanceOverTimeInfo("#performance-over-time-chart");
    result_object.createCharwiseErrorInfo("#wordwise-error-info");

    var distr_chart_radar = result_object.createMistakeDistributionInfo("#error-distribution-chart-radar", "radar");
    var distr_chart_bar = result_object.createMistakeDistributionInfo("#error-distribution-chart-bar", "bar");
    // EventHandler for Error Distribution Tabpanel, that reinitializes the charts such that they are visible. Ugly but necessary Workaround
    $(document).ready(function() {
    	$('#error-distr-radar-tab').click(function (e) {
    		e.preventDefault();
            $(this).tab('show');
            $("#error-distribution-chart-radar").find('canvas').remove();
            distr_chart_radar.destroy();
            distr_chart_radar = result_object.createMistakeDistributionInfo("#error-distribution-chart-radar", "radar");
    	});

        $('#error-distr-bar-tab').click(function (e) {
    		e.preventDefault();
            $(this).tab('show');
            distr_chart_bar.destroy();
            $("#error-distribution-chart-bar").find('canvas').remove();
            distr_chart_bar = result_object.createMistakeDistributionInfo("#error-distribution-chart-bar", "bar");
    	});
    });

}


$(document).ready(function () {
    /*

    AJAX HANDLING, FORM LISTENER
    INITITALISES WHOLE PROCESS

    */

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

        //SEND AND RECEIVE DATA FROM SERVER
        $.ajax({
            url: action,
            data: {data: JSON.stringify(data)},
            type: method
        }).fail(function (a,b,c){
            console.log("ERROR: ", a.responseText);
            requestErrorInfo("f_analysis_create_analysis", "Server Request Failed");
        }).done(function (res){
            var loadingbar = $("#loading-bar .progress-bar");
            loadingbar.stop();
            console.log("RESULT: ",res);
            loadingbar.animate({ width: "100%" }, {easing: "linear", duration: 100, complete: function () {
                toggleViews("#analysis-container");
                createAnalysis(res);
                $("#res-switch").addClass("active");
                $("#dict-switch").removeClass("active");
            }});
        });
    });
});
