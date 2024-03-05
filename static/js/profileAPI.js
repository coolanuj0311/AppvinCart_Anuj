document.addEventListener('DOMContentLoaded', function() {
    // Add your JavaScript code here
    console.log('Profile page loaded.');

    // Example: Fetch additional user data or perform other actions
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // You may need to include additional headers such as Authorization if needed
        }
    })
    .then(response => response.json())
    .then(data => {
        // Handle response data
        console.log('User profile data:', data);
        // Update the DOM with the user profile data
        document.getElementById('email').textContent = data.email;
        document.getElementById('name').textContent = data.name;
        // Update additional profile information fields as needed
    })
    .catch(error => {
        // Handle errors
        console.error('Error fetching user profile data:', error);
    });
});
