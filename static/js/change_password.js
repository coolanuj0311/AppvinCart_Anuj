document.addEventListener('DOMContentLoaded', function() {
    const changePasswordForm = document.getElementById('changePasswordForm');
    const changePasswordMessage = document.getElementById('changePasswordMessage');

    changePasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmNewPassword = document.getElementById('confirmNewPassword').value;

        if (newPassword !== confirmNewPassword) {
            changePasswordMessage.textContent = "New password and confirm new password don't match.";
            return;
        }

        fetch('/changepassword/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // You may need to include additional headers such as Authorization if needed
            },
            body: JSON.stringify({
                currentPassword: currentPassword,
                newPassword: newPassword,
                confirmNewPassword: confirmNewPassword
            })
        })
        .then(response => {
            if (response.ok) {
                // Password changed successfully
                changePasswordMessage.textContent = "Password changed successfully.";
                // Optionally, you can redirect the user to another page after successful password change
                // window.location.href = '/success-page/';
            } else {
                // Error changing password
                changePasswordMessage.textContent = "Error changing password. Please try again.";
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Error changing password:', error);
            changePasswordMessage.textContent = "Error changing password. Please try again.";
        });
    });
});
