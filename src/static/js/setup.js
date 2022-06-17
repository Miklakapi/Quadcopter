const socket = io.connect('http://192.168.1.185:5000');

$(document).ready(function () {

}).on('click', 'button', function () {
	socket.send($(this).attr('class')); //TODO
}).on('change', '.slider', function () {
	let val = $(this).val();
	$('.power').html(val + ' %');
    socket.send((5 + (5 * val / 100)).toFixed(2)); //TODO
});
