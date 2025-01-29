var id_count = 0;
var question_id_count = 0;
var entry_divs = []
var question_divs = []
var currentQuiz = {}

var recommendations = []

var currentQuizID = -1









// ON PAGE LOAD //
function onPageLoad() {
  let url_quiz_name = document.querySelector("meta[name='url-params']").dataset.url_quiz_name
  if (url_quiz_name != "*") {
    getData(url_quiz_name)
    
  }
  refreshRecs()
}









// ENTRY MANIPULATION //
function addEntry(term_text="", def_text="") {
  const termParent = document.querySelector(".termParent");

  var entry_div = document.createElement("div");
  entry_div.style = "white-space: nowrap;";
  entry_div.id = "entry_div" + String(id_count)
  entry_div.className="term-definition-div"
  entry_divs.push(entry_div);

  //Creates a term input with:
  //Type text, class term
  var termInput = document.createElement("textarea");
  termInput.className = "term input-box";
  termInput.autosize = true;
  termInput.value = term_text;
  termInput.rows="1"
  //This automatically resizes the input
  
  termInput.oninput = function() {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight-10) +'px';
    
  }
  //Creates a definition input with:
  //Type text, class definition
  var defInput = document.createElement("textarea");
  defInput.className = "definition input-box";
  defInput.autosize = true;
  defInput.value = def_text;
  defInput.rows="1"
  defInput.oninput =function() {
    this.style.height = "auto"; 
    this.style.height = (this.scrollHeight-10) +'px';
  }

  //Creates a button to remove the entry, with onclick calling removeEntry and referencing the button's id, with:
  //Type button, class removebutton
  var removeButton = document.createElement("button")
  removeButton.type = "button";
  removeButton.innerHTML = "X";
  removeButton.className = "removebutton";
  removeButton.setAttribute('onclick','registerRemoveEntry(this)')

  //Adds 1 to the ID counter
  id_count++;

  //Adds a div to the termParent
  termParent.appendChild(entry_div);

  //Adds termInput, defInput and removeButton to div
  entry_div.appendChild(termInput);
  entry_div.appendChild(defInput);
  entry_div.appendChild(removeButton);
}

function registerRemoveEntry(buttonPressed) {
  let div = buttonPressed.parentElement
  
  let removeid = String(div.id).substring(9)
  removeEntry(removeid)
  
}

function loadEntries(entries) {
  removeAllEntries()
  for (let entry of Object.keys(entries)) {
    //Iterates through keys (terms) of entries dictionary
    //Adds an entry with term text and definition
    addEntry(entry, entries[entry])
  }
}

function removeEntry(removeid) {
  let divRemove = document.getElementById("entry_div" + String(removeid));
  entry_divs = removeItem(entry_divs, divRemove)
  divRemove.remove();
  
  for (let div of entry_divs) {
    let divID = Number(String(div.id).substring(9))
    if (divID > Number(removeid)) {
      div.id = "entry_div" + String(divID - 1);
    }
  }
  id_count = id_count - 1
}

function removeAllEntries() {
  for (let i = 0; i < 9999; i++) {
    let divRemove = document.getElementById("entry_div" + String(i));
    if (document.getElementById("entry_div" + String(i)) == null) {
      break
    }
    entry_divs = removeItem(entry_divs, divRemove)
    divRemove.remove()
  }
  entry_divs = []
  id_count = 0
}
function getEntries() {
  let output = { };
  for (let i = 0; i < id_count; i++) {
    
    let div = document.getElementById("entry_div" + String(i));
    let term = div.querySelector(".term").value;
    let def = div.querySelector(".definition").value;
    output[term] = def;
    
  }
  return output
}

async function loadQuizData(data){
  let email = data["user"]["email"]
  let quiz_creator_uid = data["user"]["uid"]



  let session_user_id = JSON.parse(await fetch('/authenticator', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"mode": "getsessioninfo"})
  })
  .then(response => response.text())
  .catch(error => {
    console.error('Error:', error);
  }))

  let perms = "Cannot edit"
  if (session_user_id["uid"] == quiz_creator_uid){
    perms = "Can edit"
  }
  document.querySelector(".quiz_email").innerHTML = email
  document.querySelector(".quiz_perms").innerHTML = perms
}










//PLAY SAVE AND LOAD QUIZZES

async function playQuiz(){
  //let random_seq = (Math.random() + 1).toString(36)
  //let unique_id = random_seq.concat(String(Date.now()))

  let filename = await sendData("", currentQuizID, "True")
  let quiz_name = document.getElementById("name").value
  let entries = getEntries()

  post("/quiz", {
    "data": JSON.stringify(entries),
    "name": quiz_name,
    "filename": filename,
    "original_filename": currentQuizID,
    "unique_id": "True",
  })
}
function saveQuiz(){
  let name = document.getElementById("name").value;
  sendData(name, currentQuizID)
}
function loadQuiz(filename) {
  getData(filename)
  window.history.pushState({}, "", `/?quiz=${currentQuizID}`)
}
function loadQuizUsingFilenameInput() {
  let filename = document.getElementById("filenameInput").value
  getData(filename)
  window.history.pushState({}, "", `/?quiz=${currentQuizID}`)
}









//DATA MANIPULATION //

async function sendData(quiz_name, filename_, unique_id="False") {
  
  let output = getEntries()
  let final_filename = ""
  final_filename = await fetch('/uploader', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({name: quiz_name, filename: filename_, data: output, temporary: unique_id})
    })
    .then(response => response.text())
    .catch(error => {
      console.error('Error:', error);
    });
  
  return final_filename
}

function getData(filename) {
  currentQuizID = filename
  fetch('/uploader?' + new URLSearchParams({
    filename_to_get: filename,
    
    file_is_temporary: "False"
  }).toString())
  .then(response => response.json())
  .then(data => {
    document.getElementById("name").value = data["quiz_name"]
    loadEntries(data["quiz_data"])
    loadQuizData(data)
  })
  .catch(error => {
    console.error('Error:', error);
  });
  
}

function post(path, params, method='POST') {
  const form = document.createElement('form');
  form.method = method;
  form.action = path;

  for (const key in params) {
    if (params.hasOwnProperty(key)) {
      const hiddenField = document.createElement('input');
      hiddenField.type = 'hidden';
      hiddenField.name = key;
      hiddenField.value = params[key];

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}

function removeItem(arr, value) {
  var index = arr.indexOf(value);
  if (index > -1) {
    arr.splice(index, 1);
  }
  return arr;
}




//SEARCH QUIZZES

async function refreshRecs() {
  let sidebar_div = document.querySelector(".sidebar")
  let query = document.querySelector(".search_bar").value
  let newRecommendations = await fetch('/quiz_searcher?' + new URLSearchParams({
      search_query: query,
    }).toString())
    .then(response => response.json())
    .catch(error => {
      console.error('Error:', error);
    });
  console.log(newRecommendations)
  

  for (const recElement of recommendations) {
    recElement.remove()
  }
  
  recommendations = []

  for (const [closeness, rec_] of Object.entries(newRecommendations)) {

    var recDiv = document.createElement("div")
    recDiv.className = "quizRecommendationDiv"

    var recButton = document.createElement("button")
    recButton.type = "button";
    console.log(rec_)
    recButton.innerHTML = `${rec_["data"]["quiz_name"]}`;
    recButton.id = `button_load${rec_["id"]}`
    recButton.setAttribute('onclick','registerLoadQuiz(this)')


    recommendations.push(recButton)


    sidebar_div.appendChild(recDiv)
    recDiv.appendChild(recButton)
  }
  
  
}

function registerLoadQuiz(button) {
  let id_to_load = button.id.substring(11)
  loadQuiz(id_to_load)
}