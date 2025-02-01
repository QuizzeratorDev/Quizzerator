
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
    
});
    

function joinRoom() {
    roomID = document.querySelector(".quiz-id-input").value
    currentRoomID = roomID
    socket.emit("join", {room: roomID})
}

function createRoom() {
    socket.emit("create", {})
    setInterval(function() {
        updateRoomListForAllUsers()
    }, 1000);
}

function updateRoomListForAllUsers() {
    socket.emit("get_room_info", {
        "room": currentRoomID,
    })
}

function updateRoomList(room_users) {
    userParent.innerHTML = ""
    for (let user of room_users.values()) {
        createUserElement(user["display_name"])
    }
    
}

function updateRoomIDDisplay(room_id) {
    let roomIDDisplay = document.querySelector(".room-id-display")
    roomIDDisplay.innerHTML = room_id
}

function createUserElement(user) {
    let newUserDiv = document.createElement("div")
    let newUserName = document.createElement("p")
    newUserName.innerHTML = user
    

    newUserDiv.appendChild(newUserName)
    userParent.appendChild(newUserDiv)
    
}