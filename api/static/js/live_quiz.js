
var socket = io()

var userParent = null

var currentRoomID = null



$(document).ready(function(){ 

    

    userParent = document.querySelector(".user-list")
    console.log("initialised document")
    

    socket.on('room_data', function(msg) {
        updateRoomList(msg.data)
        
    });

    socket.on('room_creation_data', function(msg) {
        updateRoomIDDisplay(msg.data)
    });

    socket.on('receive_message_from_host', function(msg) {
        updateMessageDisplay(msg.data)
    });
    
});
    

function joinRoom() {
    roomID = document.querySelector(".quiz-id-input").value
    currentRoomID = roomID
    socket.emit("join", {room: roomID})
}


function updateRoomList(room_users) {
    userParent.innerHTML = ""
    for (let user of room_users.values()) {
        createUserElement(user["display_name"])
    }
    
}



function updateMessageDisplay(message) {
    let message_display = document.querySelector(".message-display")
    message_display.innerHTML = message
}

function updateRoomIDDisplay(room_id) {
    let roomIDDisplay = document.querySelector(".room-id-display")
    roomIDDisplay.innerHTML = room_id
    currentRoomID = room_id
}

function createUserElement(user) {
    let newUserDiv = document.createElement("div")
    let newUserName = document.createElement("p")
    newUserName.innerHTML = user
    

    newUserDiv.appendChild(newUserName)
    userParent.appendChild(newUserDiv)
    
}

