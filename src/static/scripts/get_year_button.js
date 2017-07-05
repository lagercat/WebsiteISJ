// Function for get year on EDU button
$(document).ready(function(){
	var button = document.getElementById('edu-year');
	var current_date = new Date();
	var year = current_date.getFullYear();
	button.innerHTML = year;
})