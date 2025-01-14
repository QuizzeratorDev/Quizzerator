async function markQuestion(question_attempt, answer_attempt) {
  let quiz_data = document.querySelector("meta[name='quiz-data']")
  
  let quiz_dic = quiz_data.dataset.quiz_dic
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
  let div = buttonPressed.parentElement
  let answer = div.querySelector(".answerInput").value
  let question = div.querySelector("meta[name='question-meta']").dataset.question
  //let result = markQuestion(question, answer)

  result = await markQuestion(question, answer)

  div.querySelector(".answerStatus").innerHTML = result["Output"]
  div.querySelector(".correctAnswer").hidden = true
  if (result["Output"] == "Incorrect") {
    div.querySelector(".correctAnswer").hidden = false
    div.querySelector(".correctAnswer").innerHTML = " Correct Answer is: ".concat(result["Answer"])
  }
  
  
}