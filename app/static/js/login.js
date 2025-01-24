
async function signup(){
    let _email = document.querySelector(".emailInput").value
    let _password = document.querySelector(".passwordInput").value
    let uuid = await fetch('/authenticator', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({mode: "signup", email: _email, password: _password})
    })
    .then(response => response.text())
    .catch(error => {
    console.error('Error:', error);
    });
    
    console.log(uuid)

}
