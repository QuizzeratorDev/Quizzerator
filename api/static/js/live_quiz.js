var socket = io();
var userParent = null;
var currentRoomID = null;
var currentQuestion = 0;

$(document).ready(function(){ 
    let join_room = document.querySelector(".join-room");
    join_room.hidden = false;

    let room_info = document.querySelector(".room-info");
    room_info.hidden = false;

    let question_display = document.querySelector(".live-quiz-question");
    question_display.hidden = true;

    let answer_display = document.querySelector(".answer-reveal");
    answer_display.hidden = true;

    document.querySelector(".question-submit").hidden = true;
    document.querySelector(".live-quiz-question").hidden = true;

    userParent = document.querySelector(".user-list");
    console.log("initialised document");

    socket.on('room_data', function(msg) {
        updateRoomList(msg.data);
    });

    socket.on('room_creation_data', function(msg) {
        updateRoomIDDisplay(msg.data);
    });

    socket.on('receive_message_from_host', function(msg) {
        updateMessageDisplay(msg.data);
    });

    socket.on('receive_question', function(msg) {
        updateQuestion(msg.data);
    });
    
    socket.on('reveal_answer', function(msg) {
        updateAnswerReveal(msg.data["valid"], msg.data["answer"]);
    });

    socket.on('start_quiz', function(msg) {
        startLiveQuiz();
    });
});

function joinRoom() {
    roomID = document.querySelector(".quiz-id-input").value;
    currentRoomID = roomID;
    socket.emit("join", {room: roomID});
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

function updateRoomIDDisplay(room_id) {
    let roomIDDisplay = document.querySelector(".room-id-display");
    roomIDDisplay.innerHTML = room_id;
    currentRoomID = room_id;
}

function createUserElement(user) {
    let newUserDiv = document.createElement("div");
    let newUserName = document.createElement("p");
    newUserName.innerHTML = user;
    newUserDiv.appendChild(newUserName);
    userParent.appendChild(newUserDiv);
}

function updateQuestion(question) {
    let questionDiv = document.querySelector(".live-quiz-question");
    questionDiv.hidden = false;
    let questionDisplay = document.querySelector(".question-display");
    questionDisplay.innerHTML = question["question"];
    currentQuestion = question["question_num"];
    let answer_display = document.querySelector(".answer-reveal");
    answer_display.hidden = true;
    document.querySelector(".question-submit").hidden = true;
}

function submitAnswer() {
    let answerInput = document.querySelector(".answer-input");
    let answer_ = answerInput.value;
    socket.emit("submit_answer", {answer: answer_, question_num: currentQuestion});
    
    document.querySelector(".question-submit").hidden = false;
    document.querySelector(".live-quiz-question").hidden = true;
}

function updateAnswerReveal(valid, actual_answer) {
    let answerReveal = document.querySelector(".answer-reveal");
    answerReveal.hidden = false;
    
    // Remove any existing animation classes
    answerReveal.classList.remove('answer-correct', 'answer-incorrect');
    
    if (valid) {
        answerReveal.innerHTML = "CORRECT";
        answerReveal.classList.add('answer-correct');
    } else {
        answerReveal.innerHTML = `INCORRECT! The answer was ${actual_answer}`;
        answerReveal.classList.add('answer-incorrect');
    }
}

function startLiveQuiz() {
    let join_room = document.querySelector(".join-room");
    join_room.hidden = true;

    let room_info = document.querySelector(".room-info");
    room_info.hidden = true;

    let question_display = document.querySelector(".live-quiz-question");
    question_display.hidden = false;

    let answer_display = document.querySelector(".answer-reveal");
    answer_display.hidden = true;

    document.querySelector(".question-submit").hidden = true;
    document.querySelector(".live-quiz-question").hidden = false;
}