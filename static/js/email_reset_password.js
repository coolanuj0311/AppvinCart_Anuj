document.addEventListener('DOMContentLoaded', function() {
    const resetPasswordForm = document.getElementById('resetPasswordForm');
    const resetPasswordMessage = document.getElementById('resetPasswordMessage');

    resetPasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const email = document.getElementById('email').value;

        // Send email reset password request to the backend
        fetch('/send-reset-password-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => {
            if (response.ok) {
                // Password reset link sent successfully
                resetPasswordMessage.textContent = "Password reset link sent. Please check your email.";
            } else {
                // Error sending password reset link
                resetPasswordMessage.textContent = "Error sending password reset link. Please try again.";
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Error sending password reset link:', error);
            resetPasswordMessage.textContent = "Error sending password reset link. Please try again.";
        });
    });
});
