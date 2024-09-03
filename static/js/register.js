const usernameField = document.querySelector('#username');
const invalidFeedback = document.querySelector('.invalid-feedback');

const emailField = document.querySelector('#email');
const EmailFeedback = document.querySelector('.email-invalid-feedback');

const submitButton = document.querySelector('.submit-btn');

usernameField.addEventListener('keyup', (e) => {
    const username = e.target.value;
    usernameField.classList.remove('border-red-500', 'text-red-600');
    invalidFeedback.style.display = "none";
    if (username.length > 0) {
        fetch("/auth/username-validation/", {
            body: JSON.stringify({ username: username }),
            method: "POST",
        }).then(res => res.json()).then(data => {
            if (data.username_error) {
                submitButton.disabled = true;
                usernameField.classList.add('border-red-500', 'text-red-600');
                invalidFeedback.style.display = 'block';
                invalidFeedback.innerHTML = `<p class="text-red-600">${data.username_error}</p>`;
            } else {
                submitButton.removeAttribute("disabled");
            }
        });
    }
});

emailField.addEventListener('keyup', (e) => {
    const email = e.target.value;
    emailField.classList.remove('border-red-500', 'text-red-600');
    EmailFeedback.style.display = "none";
    if (email.length > 0) {
        fetch("/auth/email-validation/", {
            body: JSON.stringify({ email: email }),
            method: "POST",
        }).then(res => res.json()).then(data => {
            if (data.email_error) {
                submitButton.disabled = true;
                emailField.classList.add('border-2','border-red-500', 'text-red-600');
                EmailFeedback.style.display = 'block';
                EmailFeedback.innerHTML = `<p class="text-red-600">${data.email_error}</p>`;
            } else {
                submitButton.removeAttribute("disabled");
            }
        });
    }
});
