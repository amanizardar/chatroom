document.addEventListener('DOMContentLoaded', () => {

    
    const request = new XMLHttpRequest();
    request.open("POST", "/listmessages");


    request.onload = () => {
        const data = JSON.parse(request.responseText);
        localStorage.setItem("chat_id", data["chat_id"])
        let i;
        for ( i=0; i<data["message"].length; i++) {
            const li = document.createElement('li');
            const response = data["message"][i];


            li.innerHTML = `<strong>${response["user_name"]}</strong> : <span class="mx-4"><big>${response["selection"]}</big></span> <small>${response["time"]}</small>`;
            document.querySelector('#messages').append(li);
        }
    };
    request.send();



 
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  
    socket.on('connect', () => {

   
        document.querySelector('button').onclick = function () {
            const selection = document.querySelector('input').value;
            this.form.reset();
            socket.emit('submit message', {'selection': selection});
        };
    });

    socket.on ('cast message', data => {
        if (data["chat_id"] === localStorage.chat_id) {
            const li = document.createElement('li');

 
            li.innerHTML = `<strong>${data["user_name"]}</strong> : <span class="mx-4"><big>${data["selection"]}</big></span> <small>${data["time"]}</small>`;
            document.querySelector('#messages').append(li);
        }
    });


});
