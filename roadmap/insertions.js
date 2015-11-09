$(document).ready(function () {
	
	// INSERTS CALENDAR ICON BEFORE ALL DATES
	$(".task-all.date").prepend('<i class="fa fa-calendar-check-o"></i> ');
	
	// INSERTS CLOCK ITEM BEFORE ALL DUE DATES
	$(".due-date").prepend('<i class="fa fa-clock-o"></i> ');
	
})