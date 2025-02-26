document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const errorDiv = document.getElementById('passwordError');
    const registerButton = document.getElementById('registerButton');

    form.addEventListener('submit', function(event) {
        if (password.value !== confirmPassword.value) {
            errorDiv.style.display = 'block';
            password.classList.add('is-invalid');
            confirmPassword.classList.add('is-invalid');
            event.preventDefault();
        } else {
            errorDiv.style.display = 'none';
            password.classList.remove('is-invalid');
            confirmPassword.classList.remove('is-invalid');
            registerButton.disabled = true;
        }
    });
});