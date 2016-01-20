function convertStringToHTML(str) {
    return str.replace(/\n/g, "<br>");
}

function toggleViews(to_view) {

    /*
    * Function to control the toggling between dictation form and analysis
    */

    if (!$(to_view).hasClass('main-container')) {
        $(".main-container").fadeOut(0, function () {
            $(this).removeClass("main-container");
            $(to_view).fadeIn(0, function () {
                $(this).addClass("main-container");
            });
        });
    }

}
