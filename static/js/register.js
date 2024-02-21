document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');
    const registrationMessage = document.getElementById('registrationMessage');

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        const formData = new FormData(registrationForm);

        // Send POST request to backend API
        fetch('/register/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Registration failed');
            }
        })
        .then(data => {
            // Handle successful registration response
            registrationMessage.textContent = 'Registration successful';
            
            // Redirect to login page after a short delay to show the message
            setTimeout(() => {
                window.location.href = '/login';
                 // Adjust the URL as necessary
            }, 2000); // Redirect after 2 seconds
        })
        .catch(error => {
            // Handle registration error
            registrationMessage.textContent = 'Registration failed: ' + error.message;
        });
    });
});
