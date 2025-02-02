var socket = io();
var currentRoomID = null;
var quizName = null;
var quizData = null;
var userParent = null;
var currentQuestionData = null;

$(document).ready(function(){ 
    createRoom();

    // Get quiz data from meta tags
    let quizDataMeta = document.querySelector("meta[name='host-quiz-data']");
    quizName = quizDataMeta.dataset.quiz_name;
    quizData = quizDataMeta.dataset.quiz_data;

    userParent = document.querySelector(".user-list");
    console.log("initialised document");
    

    socket.on('room_data', function(msg) {
        console.log("Received room data:", msg);
        updateRoomList(msg.data);
    });

    socket.on('room_creation_data', function(msg) {
        console.log("Received room creation data:", msg);
        updateRoomIDDisplay(msg.data);
    });

    socket.on('receive_message_from_host', function(msg) {
        updateMessageDisplay(msg.data);
    });
    
    socket.on('receive_question', function(msg) {
        updateCurrentQuestion(msg.data);
    });
});

function createRoom() {
    socket.emit("create", {});
    setInterval(function() {
        if (currentRoomID != null) {
            updateRoomListForAllUsers();
        }
    }, 5000);
}

function startLiveQuiz() {
    socket.emit("start_quiz");
    document.querySelector('.start-quiz').disabled = true;
    document.querySelector('.start-quiz').textContent = 'Quiz Started';
}

function updateCurrentQuestion(questionData) {
    currentQuestionData = questionData;
    const questionNumber = document.querySelector('.question-number');
    const questionText = document.querySelector('.question-text');
    
    if (questionData && questionData.question) {
        questionNumber.textContent = `Question ${questionData.question_num}`;
        questionText.textContent = questionData.question;
    } else {
        questionNumber.textContent = 'No Question';
        questionText.textContent = 'No question sent yet';
    }
}

function updateRoomIDDisplay(room_id) {
    let roomIDDisplay = document.querySelector(".room-id-display");
    roomIDDisplay.innerHTML = `ID: ${room_id}`;
    currentRoomID = room_id;
    console.log("Updated room ID to:", room_id);
}

function updateRoomListForAllUsers() {
    socket.emit("get_room_info", {});
}

function updateRoomList(room_users) {
    userParent.innerHTML = "";
    for (let user of room_users.values()) {
        createUserElement(user["display_name"]);
    }
}

function updateMessageDisplay(message) {
    let message_display = document.querySelector(".message-display");
    message_display.innerHTML = message;
}

function createUserElement(user) {
    let newUserDiv = document.createElement("div");
    let newUserName = document.createElement("p");
    newUserName.innerHTML = user;
    newUserDiv.appendChild(newUserName);
    userParent.appendChild(newUserDiv);
}

function sendQuestion() {
    socket.emit("host_send_question");
    
    // Reset the end answers button
    const endAnswersButton = document.querySelector('.end-answers');
    endAnswersButton.disabled = false;
    endAnswersButton.textContent = 'End Answers';
    
    // Add visual feedback for send question button
    const sendQuestionButton = document.querySelector('.send-question');
    sendQuestionButton.disabled = true;
    setTimeout(() => {
        sendQuestionButton.disabled = false;
    }, 2000);
}

function endAnswers() {
    socket.emit("host_end_answers");
    const endAnswersButton = document.querySelector('.end-answers');
    endAnswersButton.disabled = true;
    endAnswersButton.textContent = 'Answers Ended';
}

function sendMessage() {
    let messageInput = document.querySelector(".message-input");
    let message = messageInput.value.trim();
    
    if (message) {
        socket.emit("host_send_message", {message: message});
        messageInput.value = '';
    }
}