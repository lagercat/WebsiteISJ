// Function for get year on EDU button
$(document).ready(function(){
	var current_date = new Date();
	var year = current_date.getFullYear();
	$('.edu-year-button').each(function(i, obj) {
		$(this).html(year + "-" + (year + 1));
	});
})
