document.addEventListener('DOMContentLoaded', () => {

    
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

       
        document.querySelector('form button').onclick = () => {
            const selection = document.querySelector('form input').value;
            socket.emit('submit channel', {'selection': selection})
        };
    });


    socket.on ('cast channel', data => {
        const li = document.createElement('li');

        li.innerHTML = `<a href="/chatrooms/${data["chat_id"]}"> ${data["selection"]} </a>`;
        console.log(li.innerHTML);
        document.querySelector('#chatrooms').append(li);
    });
});
