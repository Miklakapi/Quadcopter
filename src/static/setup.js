//Power
$('.slider').on('input', function () {
    var percent = $('.slider').val();
    $('.power').html(percent + '%');

    var value = 5 + (5 * percent / 100);
    $.get('http://192.168.0.202:8000/power/' + value);
});

//Right
$('.right').click(function () {
	$.get('http://192.168.0.202:8000/direction/4');
});

//Left
$('.left').click(function () {
	$.get('http://192.168.0.202:8000/direction/3');
});

//Forward
$('.forward').click(function () {
	$.get('http://192.168.0.202:8000/direction/1');
});

//Backward
$('.backward').click(function () {
	$.get('http://192.168.0.202:8000/direction/2');
});

//Left rotation
$('.leftRotation').click(function () {
	$.get('http://192.168.0.202:8000/rotation/1');
});

//Right rotation
$('.rightRotation').click(function () {
	$.get('http://192.168.0.202:8000/rotation/2');
});

//Stay
$('.dot').click(function () {
	var percent = $('.slider').val();
	var value = 5 + (5 * percent / 100);
	$.get('http://192.168.0.202:8000/power/' + value);
});