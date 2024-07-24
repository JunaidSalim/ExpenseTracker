const usernameField = document.querySelector('#username')
const invalidFeedback = document.querySelector('.invalid-feedback')



usernameField.addEventListener('keyup', (e) => {
    const username = e.target.value;
    usernameField.classList.remove('is-invalid');
    invalidFeedback.style.display = "none";
    if (username.length > 0) {
        fetch("/auth/username-validation/", {
            body: JSON.stringify({ username: username }),
            method: "POST",
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.username_error) {
                usernameField.classList.add('is-invalid');
                invalidFeedback.style.display = 'block';
                invalidFeedback.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
});