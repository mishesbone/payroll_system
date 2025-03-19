document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(registerForm);
        const data = {};
        
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/employee_dashboard';
            } else {
                alert('Registration failed: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
