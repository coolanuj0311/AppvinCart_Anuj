document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');
    const registrationMessage = document.getElementById('registrationMessage');

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        const formData = new FormData(registrationForm);

        // Perform client-side form validation
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm Password');
        if (!formData.get('username') || !formData.get('password') || !formData.get('confirm Password')) {
            registrationMessage.textContent = 'Please fill out all required fields.';
            return;
        }
        if (password !== confirmPassword) {
            registrationMessage.textContent = 'Passwords do not match.';
            return;
        }

        // Send POST request to backend API
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Registration failed. Please try again later.');
            }
        })
        .then(data => {
            // Handle successful registration response
            registrationMessage.textContent = 'Registration successful';
            
            // Redirect to login page after a short delay to show the message
            setTimeout(() => {
                window.location.href = 'login';
            }, 2000); // Redirect after 2 seconds
        })
        .catch(error => {
            // Handle registration error
            registrationMessage.textContent = 'Registration failed: ' + error.message;
        });
    });
});
