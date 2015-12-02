$(document).ready(function() {
    $(".collapse button.collapse-button").click(function () {
        $(this).parent().siblings(".collapse-content").toggle();
		if ($(this).parent().siblings(".collapse-content").is(":visible")) {
			$(this).html('<button class="collapse-button"><i class="fa fa-chevron-down"></i></button>');
		} else {
			$(this).html('<button class="collapse-button"><i class="fa fa-chevron-right"></i></button>');
		}
    });
});