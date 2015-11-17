function createAnalysis(res) {
    /*
     * Function to use results of analysis and build up an evaluation page
     * for the user.
     */
    
    console.log(res);
    
    //PARSING input
    var data = res[0]["data"];
    var meta = res[0]["meta"];
    
    console.log(data);
    
    //CREATE HEADER
    var header = $("#analysis-container .page-header");
    var text_id = $("<small>");
    text_id.html("<br>For Text " + data["text_id"]); //actually want to look up real name from DB
    header.find("h3").append(text_id);
    
    //CREATE INPUT INFO
    var input_info = $("#input-info");
    console.log(data["input"]);
    var input_data_html = data["input"].replace(/\n/g, "").split(" ");
    var diff_map = data["diff_map"]
    
    var marked_input = "";
    for (word = 0; word < input_data_html.length; word++) {
        if (diff_map[word] === false) {
            marked_input += "<span class='spelling sp-wrong'>" + input_data_html[word] + "</span> ";
        } else {
            marked_input += "<span class='spelling sp-correct'>" + input_data_html[word] + "</span> ";
        }
    }
    
    input_info.find(".well").html(marked_input);
    
    //CREATE TARGET INFO
    var target_info = $("#target-info");
    console.log(data["target"]);
    var target_data_html = data["target"].replace(/\n/g, "<br>");
    target_info.find(".well").html(target_data_html);
    
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
            text_id: $("#dictation-id").val(),
            target: "Rosen sind rot und Veilchen sind blau, ich mag gerne Brot, dass ich mir oft klau"
        };
        
        var action = $(this).attr("action");
        var method = $(this).attr("method");
        
        //SEND AND RECEIVE DATA FROM SERVER
        $.ajax({
            url: action,
            data: {data: JSON.stringify(data)},
            type: method
        }).fail(function (a,b,c){
            console.log("hi");
            console.log(a,b,c);
        }).done(function (res){           
            createAnalysis(res);
            revealAnalysis();
            
        });
    });
});