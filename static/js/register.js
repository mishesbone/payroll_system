document.getElementById("registrationForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let formData = new FormData(this);
    let csrfToken = document.querySelector('input[name="csrf_token"]').value;  // Ensure it is correctly fetched

    fetch(this.action, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,  // Include CSRF token here
            "Accept": "application/json"
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Registration successful! Redirecting...");
            window.location.href = data.redirect_url || "/dashboard";  // Redirect to dashboard
        } else {
            alert(data.message || "Something went wrong.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
});
