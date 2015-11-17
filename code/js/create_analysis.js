function createAnalysis(res) {
    /*
     * Function to use results of analysis and build up an evaluation page
     * for the user.
     */
    
    //PARSING input
    var res_object = $.parseJSON(res);
    var data = res_object["data"];
    var meta = res_object["meta"];
    
    //CREATE HEADER
    var header = $("#analysis-container .page-header");
    var text_id = $("<small>");
    text_id.html("<br>For Text " + data["text_id"]); //actually want to look up real name from DB
    header.find("h3").append(text_id);
    
    //CREATE INPUT INFO
    var input_info = $("#input-info");
    console.log(data["input"]);
    var input_data_html = data["input"].replace(/\n/g, "<br>");
    console.log(input_data_html);
    input_info.find(".well").html(input_data_html);
    
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

        var data = {
            input: $("#dictation-text").val(),
            text_id: $("#dictation-id").val()
        };
        
        var action = $(this).attr("action");
        var method = $(this).attr("method");
        
        //SEND AND RECEIVE DATA FROM SERVER
        $.ajax({
            url: action,
            data: {data: JSON.stringify(data)},
            type: method
        }).fail(function (a,b,c){
            console.log(a,b,c);
        }).done(function (res){
            console.log("Received data: " + res);
            
            createAnalysis(res);
            revealAnalysis();
            
        });
    });
});