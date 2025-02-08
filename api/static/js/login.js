import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js";



const firebaseConfig = {
    apiKey: "AIzaSyDtDf_axVxEN4A7l82c6YU9JKDH_B3cvrM",
    authDomain: "quizzerator.firebaseapp.com",
    databaseURL: "https://quizzerator-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "quizzerator",
    storageBucket: "quizzerator.firebasestorage.app",
    messagingSenderId: "643394311206",
    appId: "1:643394311206:web:39b5fa26801cee684042e7",
    measurementId: "G-XGDKKC88LQ"
};

const app = initializeApp(firebaseConfig);
async function onPageLoad() {
    document.querySelector(".password-status").innerHTML = ""
    let session_user = JSON.parse(await fetch('/authenticator', {
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
    
    console.log(session_user)
    if (session_user["email"] !="") {
        document.querySelector(".auth-card").hidden = true
        document.querySelector(".user-info").hidden = false
        document.querySelector(".signout").hidden = false
        document.querySelector(".display-name").innerHTML = `Logged in as ${session_user["display_name"]}`
    }
    else{
        document.querySelector(".auth-card").hidden = false
        document.querySelector(".user-info").hidden = true
        document.querySelector(".signout").hidden = true
        
    }
        
}
async function login_user() {
    const auth = getAuth();
    let _email = document.querySelector(".login_emailInput").value
    let _password = document.querySelector(".login_passwordInput").value
    
    let user_info = await signInWithEmailAndPassword(auth, _email, _password)
    .then((userCredential) => {
        // Signed in 
        return userCredential
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        return "Could not sign in"
    });

    if (user_info != "Could not sign in"){
        await fetch('/authenticator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({mode: "signin", userinfo: user_info})
            })
            .then(response => response.text())
            .catch(error => {
            console.error('Error:', error);
            });
        window.location.replace("/");
    }
    else {
        document.querySelector(".password-status").innerHTML = "Incorrect Email or Password!"
    }
    
}
window.addEventListener("DOMContentLoaded", () => {
const loginButton = document.getElementById("loginButton");
loginButton.addEventListener("click", login_user);
});
window.addEventListener("DOMContentLoaded", () => {
const loginButton = document.getElementById("signupButton");
loginButton.addEventListener("click", signup);
});

window.addEventListener("DOMContentLoaded", () => {
const loginButton = document.getElementById("signOutButton");
loginButton.addEventListener("click", signout);
});

window.addEventListener("DOMContentLoaded", () => {
const emailInput = document.querySelector(".login_emailInput");
emailInput.addEventListener("input", function () {
    document.querySelector(".password-status").innerHTML = ""
});
});

window.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.querySelector(".login_passwordInput");
    passwordInput.addEventListener("input", function() {
        document.querySelector(".password-status").innerHTML = ""
    });
    });

window.addEventListener("DOMContentLoaded", () => {
    onPageLoad()
});
async function signup(){
    const auth = getAuth();
    let _email = document.querySelector(".emailInput").value
    let _password = document.querySelector(".passwordInput").value
    let _username = document.querySelector(".usernameInput").value
    let uuid = await fetch('/authenticator', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({mode: "signup", username: _username, email: _email, password: _password})
    })
    .then(response => response.text())
    .catch(error => {
    console.error('Error:', error);
    });
    
    console.log(uuid)
    let user_info = await signInWithEmailAndPassword(auth, _email, _password)
    .then((userCredential) => {
        // Signed in 
        return userCredential
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        return "Could not sign in"
    });

    if (user_info != "Could not sign in"){
        await fetch('/authenticator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({mode: "signin", userinfo: user_info})
            })
            .then(response => response.text())
            .catch(error => {
            console.error('Error:', error);
            });
        window.location.replace("/");
        
    }
    

}

async function signout(){
    let uuid = await fetch('/authenticator', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({mode: "signout"})
    })
    .then(response => response.text())
    .catch(error => {
    console.error('Error:', error);
    });
    
    console.log(uuid)

    post("/", {
    })

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
  