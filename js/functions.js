function convertStringToHTML(str) {
    return str.replace(/\n/g, "<br>");
}

function countArrayDuplicates(array) {
    var counts = {};
    array.forEach(function(x) { counts[x] = (counts[x] || 0)+1; });

    return counts;
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

function loadingbar(target, delay) {
	var wrapper = $("<div>")
		.addClass('progress');

	var loadingbar = $("<div>")
		.addClass('progress-bar')
		.attr({
			role: 'progressbar',
            style: 'width: 5%;'
		});

    wrapper.append(loadingbar);
    $(target).append(wrapper);

	var current_state = 0;

    var expand_bar = function () {
        if (current_state < 99.99) {
            current_state += ((100 - current_state)/3);
            console.log(current_state);
            loadingbar.animate({ width: current_state+"%" }, {easing: "linear", duration: 3500, complete: expand_bar});
        }
    };

    expand_bar();
}

function isEmail(mail) {
    if (mail.search(/\@/) === -1) {
        return false;
    } else {
        return true;
    }
}
