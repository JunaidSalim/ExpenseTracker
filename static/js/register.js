const usernameField = document.querySelector('#username')
const invalidFeedback = document.querySelector('.invalid-feedback')

const emailField = document.querySelector('#email')
const EmailFeedback = document.querySelector('.email-invalid-feedback')

const showPassword = document.querySelector('.showPassword')
const passwordField = document.querySelector('#password')

usernameField.addEventListener('keyup', (e) => {
    const username = e.target.value;
    usernameField.classList.remove('is-invalid');
    invalidFeedback.style.display = "none";
    if (username.length > 0) {
        fetch("/auth/username-validation/", {
            body: JSON.stringify({ username: username }),
            method: "POST",
        }).then(res => res.json()).then(data => {
            if (data.username_error) {
                usernameField.classList.add('is-invalid');
                invalidFeedback.style.display = 'block';
                invalidFeedback.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
});

emailField.addEventListener('keyup', (e) => {
    const email = e.target.value;
    emailField.classList.remove('is-invalid');
    EmailFeedback.style.display = "none";
    if (email.length > 0) {
        fetch("/auth/email-validation/", {
            body: JSON.stringify({ email: email }),
            method: "POST",
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.email_error) {
                emailField.classList.add('is-invalid');
                EmailFeedback.style.display = 'block';
                EmailFeedback.innerHTML = `<p>${data.email_error}</p>`
            }
        });
    }
});

showPassword.addEventListener('click',(e) =>{
    if (showPassword.textContent==='SHOW')
    {
        showPassword.textContent = 'HIDE'
        passwordField.setAttribute("type",'text')
    }
    else{
        showPassword.textContent = 'SHOW'
        passwordField.setAttribute("type",'password')
    }

});