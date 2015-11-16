$(document).ready(function () {
    $("#dictation-form").submit(function (event) {
        event.preventDefault();
        console.log("Entered Click");
        
        //var field_data = $("#dictation-text").serialize();
        var field_data = 'data=' + "\"{ 'data' : '" + $("#dictation-text").val() + "' }\"";
        console.log(field_data);
        console.log(typeof field_data);
        var action = $(this).attr("action");
        var method = $(this).attr("method");
        console.log(action);
        
        $.ajax({
            url: action,
            data: field_data,
            type: method,
            error: function (a,b,c){console.log(a,b,c);},
            complete: function (res){console.log(res);}
            });
    });
});