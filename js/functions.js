function convertStringToHTML(str) {
    return str.replace(/\n/g, "<br>");
}

function countArrayDuplicates(array) {
    var counts = {};
    array.forEach(function(x) { counts[x] = (counts[x] || 0)+1; });

    return counts;
}

function sumArray(array) {
    var total = 0;
    $.each(array, function() {
         total += this;
    });
    return total;
}

function equalizeKeys(array_a, array_b, default_val) {
    /*
        adds all keys of a to b with value default and vice versa
     */

    for (var key_a in array_a) {
        if (!array_b.hasOwnProperty(key_a)) {
            array_b[key_a] = default_val;
        }
    }

    for (var key_b in array_b) {
        if (!array_a.hasOwnProperty(key_b)) {
            array_a[key_b] = default_val;
        }
    }

    return [array_a, array_b];
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
