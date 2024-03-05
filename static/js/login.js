document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginMessage = document.getElementById('loginMessage');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        const formData = new FormData(loginForm);

        // Send POST request to backend API
        fetch('/login/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Login failed');
            }
        })
        .then(data => {
            // Handle successful login response
            loginMessage.textContent = 'Login successful';
            // Optionally, redirect the user to another page after successful login
            setTimeout(() => {
                window.location.href = 'store';
                 // Adjust the URL as necessary
            }, 2000); // Redirect after 2 seconds
        
            
        })
        .catch(error => {
            // Handle login error
            loginMessage.textContent = 'Login failed: ' + error.message;
            setTimeout(() => {
                window.location.href = 'login';
                 // Adjust the URL as necessary
            }, 2000); // Redirect after 2 seconds
        
        });
    });
});