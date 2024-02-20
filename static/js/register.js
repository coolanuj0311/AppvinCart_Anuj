
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('registrationForm').addEventListener('submit', function (event) {
        event.preventDefault();
        // Perform registration form submission here (e.g., AJAX request to server)

        // For demonstration purposes, let's assume registration is successful
        // and display the popup message
        $('#registrationSuccessModal').modal('show');

        // Clear the form fields
        document.getElementById('registrationForm').reset();
    });
});



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
        })
        .catch(error => {
            // Handle registration error
            registrationMessage.textContent = 'Registration failed: ' + error.message;
        });
    });
});
