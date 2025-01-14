function addQuestion(term, definition) {
    let quiz_div = document.getElementById(quiz)
    
    let question_div = document.createElement("div")
    question_div.id = "question_div" + String(question_id_count)
  
    let questionLabel = document.createElement("label")
    questionLabel.class = "questionLabel"
    questionLabel.innerHTML = String(term)
  
    let answerInput = document.createElement("input")
    answerInput.class = "answerInput"
    answerInput.type = "text";
  
    quiz_div.appendChild(question_div)
  
    question_div.appendChild(questionLabel)
    question_div.appendChild(answerInput)
    question_div.appendChild(answerLabel)
  
  }