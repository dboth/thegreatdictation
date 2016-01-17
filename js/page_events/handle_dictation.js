$(document).ready(function () {
    // by default HIDE audioplayer
    $("#audio-player").hide();

    //ENABLE Select Button on preselection
    $("#dictation-id").change(function () {
        $("#select-text-button").removeAttr("disabled");
    });

    //DISABLE Select and Select Button on selection and SHOW audioplayer and ENABLE the dictation
    $("#select-text-button").click(function () {
        $("#dictation-id").attr("disabled", "disabled");
        $("#select-text-button").attr("disabled", "disabled");

        $("#audio-player").show();

        $("#dictation-text").removeAttr("disabled");
        $("#dictation-submit").removeAttr("disabled");
    });

    //SWAP between views
    $("#dict-switch").click(function () {
        toggleViews("#dictation-container");
        $("#dict-switch").addClass("active");
        $("#res-switch").removeClass("active");
    });

    $("#res-switch").click(function () {
        toggleViews("#analysis-container");
        $("#res-switch").addClass("active");
        $("#dict-switch").removeClass("active");
    });
});
