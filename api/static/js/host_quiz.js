var socket = io()

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

function createRoom() {
    socket.emit("create", {})
    setInterval(function() {
        if (currentRoomID != null) {
            updateRoomListForAllUsers()
        }
        
    }, 5000);
}

function updateRoomIDDisplay(room_id) {
    let roomIDDisplay = document.querySelector(".room-id-display")
    roomIDDisplay.innerHTML = room_id
    currentRoomID = room_id
}

function updateRoomListForAllUsers() {
    socket.emit("get_room_info", {
    })
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

function createUserElement(user) {
    let newUserDiv = document.createElement("div")
    let newUserName = document.createElement("p")
    newUserName.innerHTML = user
    

    newUserDiv.appendChild(newUserName)
    userParent.appendChild(newUserDiv)
    
}



function sendMessage() {
    let message_ = document.querySelector(".message-input").value
    socket.emit("host_send_message", {message: message_})
}