function createAnalysis(res) {

    /*
     * Function to use results of analysis and build up an evaluation page
     * for the user.
     */

    var result_object = new Result(res[0]);

    result_object.createHeader("#analysis-container .page-header");
    result_object.createAlignmentInfo("#input-info-container");
    result_object.createOverallScoreInfo("#score-info");
    result_object.createMistakeDistributionInfo("#error-distribution-chart", "bar");
    result_object.createPerformanceOverTimeInfo("#performance-over-time-chart");
    result_object.createWordwiseErrorInfo("#wordwise-error-info");

    // var target_info = $("#target-info");
	// target_info.find(".well").html(convertStringToHTML(result_object.target));
}


$(document).ready(function () {
    /*

    AJAX HANDLING, FORM LISTENER
    INITITALISES WHOLE PROCESS

    */

    $("#dictation-form").submit(function (event) {
        event.preventDefault();

        var data = {
            input: $("#dictation-text").val().replace(/\s$/, ""),
            text_id: $("#dictation-id").val(),
            target: ""
        };

        var action = $(this).attr("action");
        var method = $(this).attr("method");

        //SEND AND RECEIVE DATA FROM SERVER
        $.ajax({
            url: action,
            data: {data: JSON.stringify(data)},
            type: method
        }).fail(function (a,b,c){
            console.log("ERROR: ", a.responseText);
            requestErrorInfo("f_analysis_create_analysis", "Server Request Failed");
        }).done(function (res){
            console.log("RESULT: ",res);
            createAnalysis(res);
            toggleViews("#analysis-container");
            $("#res-switch").addClass("active");
            $("#dict-switch").removeClass("active");
        });
    });
});
