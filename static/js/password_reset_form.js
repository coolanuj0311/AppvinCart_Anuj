document.addEventListener('DOMContentLoaded', function() {
    const passwordResetForm = document.getElementById('passwordResetForm');
    const passwordResetMessage = document.getElementById('passwordResetMessage');

    passwordResetForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const uid = document.querySelector('input[name="uid"]').value;
        const token = document.querySelector('input[name="token"]').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            passwordResetMessage.textContent = "New password and confirm new password don't match.";
            return;
        }

        // Send password reset request to the backend
        fetch(`/reset-password/<uid>/<token>/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password, password2: confirmPassword })
        })
        .then(response => {
            if (response.ok) {
                // Password reset successfully
                passwordResetMessage.textContent = "Password reset successfully.";
                // Optionally, you can redirect the user to the login page or any other page
                // window.location.href = '/login/';
            } else {
                // Error resetting password
                passwordResetMessage.textContent = "Error resetting password. Please try again.";
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Error resetting password:', error);
            passwordResetMessage.textContent = "Error resetting password. Please try again.";
        });
    });
});
