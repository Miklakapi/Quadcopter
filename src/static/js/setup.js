$(document).ready(function () {
}).on('click', 'button', function () {
	$.get('http://192.168.1.185:5000/direction/' + $(this).attr('class'));
}).on('change', '.slider', function () {
	let val = $(this).val();
	$('.power').html(val + '%');
	$.get('http://192.168.1.185:5000/power/' + (5 + (5 * val / 100)));
});
