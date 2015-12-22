function createAnalysis(res) {

    /*
     * Function to use results of analysis and build up an evaluation page
     * for the user.
     */

    var result_object = new Result(res[0]);

    result_object.createHeader("#analysis-container .page-header");
    result_object.createLevenshteinDiffInfo("#error-indication");
    result_object.createOverallScoreInfo("#score-info");

    var target_info = $("#target-info");
	target_info.find(".well").html(convertStringToHTML(result_object.target));
}

function revealAnalysis() {

    /*
    * Function to control the toggling between dictation form and analysis
    */

    $("#dictation-container").fadeOut("fast", function () {
        $("#analysis-container").fadeIn("fast");
    });

}

$(document).ready(function () {
    /*

    AJAX HANDLING, FORM LISTENER
    INITITALISES WHOLE PROCESS

    */

    $("#dictation-form").submit(function (event) {
        event.preventDefault();

        var tests = ["Rosen sind rot und Veilchen sind blau, ich mag gerne Brot, das ich mir oft klau", "Ich bin ein Elefant", "Dieses Projekt übersteigt alles in Awesomenesshaftigkeit"];

        var data = {
            input: $("#dictation-text").val().replace(/\s$/, ""),
            text_id: $("#dictation-id").val(),
            target: tests[$("#dictation-id").val()]
        };

        var action = $(this).attr("action");
        var method = $(this).attr("method");

        //SEND AND RECEIVE DATA FROM SERVER
        $.ajax({
            url: action,
            data: {data: JSON.stringify(data)},
            type: method
        }).fail(function (a,b,c){
            console.log("ERROR IN AJAX\n---------------");
            console.log("received object: ", a);
            console.log("Error msg: ", b);
            console.log("ERROR TYPE: ", c);
        }).done(function (res){
            console.log("SUCCESS");
            createAnalysis(res);
            revealAnalysis();
        });
    });
});
