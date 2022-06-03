let interval;

$(document).ready(function () {
    interval = setInterval(initPower, 500);
});

function initPower() {
    fetch('http://192.168.1.6:5000/get-data')
    .then(async response => {

        if (!response.ok) {
            let status = response.status;
            return Promise.reject(status);
        }
        
        const responseData = await response.json();

        putData(responseData);
    })
    .catch(error => {
        $('.error').html('Error while downloading data!');
        clearInterval(interval);
    });
}

function putData(data) {
    $('.engine:nth-child(1)').html(data['1']);
    $('.engine:nth-child(2)').html(data['2']);
    $('.engine:nth-child(3)').html(data['3']);
    $('.engine:nth-child(4)').html(data['4']);
}
