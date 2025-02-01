
var socket = io()

$(document).ready(function(){ 
    console.log("initialised document")
    socket.on('toast_messages', function(msg) {
        console.log(msg.data)
    });
    
});
    

function sendData() {

    socket.emit("join", {username: "crazycat", room: "room123"})
}
