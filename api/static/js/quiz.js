async function markQuestion(question_attempt, answer_attempt) {
  let quiz_data = document.querySelector("meta[name='quiz-data']")
  
  let quiz_name_ = quiz_data.dataset.quiz_filename

  const output = await fetch('/quiz_master?' + new URLSearchParams({
    quiz_name: quiz_name_,
    question: question_attempt,
    answer: answer_attempt
  }).toString())
  .catch(error => {
    console.error('Error:', error);
  });

  const data = await output.json()
  return data

}

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}

async function registerMarkQuestion(buttonPressed) {
    let questionCard = buttonPressed.closest('.question-card');
    let div = buttonPressed.parentElement;
    let answer = div.querySelector(".answerInput").value;
    let question = questionCard.querySelector("meta[name='question-meta']").dataset.question_num;

    result = await markQuestion(question, answer);

    let answerStatus = questionCard.querySelector(".answerStatus");
    let correctAnswer = questionCard.querySelector(".correctAnswer");
    
    // Remove previous styling
    questionCard.classList.remove('correct', 'incorrect');
    answerStatus.classList.remove('correct', 'incorrect');
    
    if (result["Output"] === "Correct") {
        questionCard.classList.add('correct');
        answerStatus.classList.add('correct');
        correctAnswer.hidden = true;
    } else {
        questionCard.classList.add('incorrect');
        answerStatus.classList.add('incorrect');
        correctAnswer.hidden = false;
        correctAnswer.innerHTML = "Correct Answer: " + result["Answer"];
    }
    
    answerStatus.innerHTML = result["Output"];
    answerStatus.hidden = false;
}

function returnToIndex() {
  let quiz_data = document.querySelector("meta[name='quiz-data']")
  fetch('/quiz_master', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({filename: quiz_data.dataset.quiz_filename})
  })
  .then(response => response.text())
  .catch(error => {
    console.error('Error:', error);
  });
  original_filename = quiz_data.dataset.original_filename
  window.location.replace(`/?quiz=${original_filename}`);
}

//This code does not work
window.onbeforeunload = function(){

  //This deletes the temporary quiz session file on window unload
  fetch('/quiz_master', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({filename: quiz_data.dataset.quiz_filename})
  })
  .then(response => response.text())
  .catch(error => {
    console.error('Error:', error);
  });
}