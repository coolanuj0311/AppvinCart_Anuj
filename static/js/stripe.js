// Initialize Stripe.js with your publishable key
var stripe = Stripe('pk_test_51OjyPXSHvzT4MJlEa98zk4ckAM6Mr4w3jWXJemFxFg9LmIKsJs5zIrzzyA3CPo3nU931Or7jlHhDwIxVKcBoyV0v00YVRQ4H9B');

// Function to handle the submission of the payment form
function handleFormSubmission(form) {
    // Disable the submit button to prevent multiple submissions
    var submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    // Extract the card element from the form
    var cardElement = form.querySelector('#card-element');

    // Create a token from the card element
    stripe.createToken(cardElement).then(function(result) {
        // If an error occurs during token creation, display the error message
        if (result.error) {
            var errorElement = form.querySelector('#card-errors');
            errorElement.textContent = result.error.message;
            submitButton.disabled = false; // Re-enable the submit button
        } else {
            // If token creation is successful, append the token to the form and submit the form
            var tokenInput = document.createElement('input');
            tokenInput.setAttribute('type', 'hidden');
            tokenInput.setAttribute('name', 'stripeToken');
            tokenInput.setAttribute('value', result.token.id);
            form.appendChild(tokenInput);
            form.submit();
        }
    });
}

// Function to initialize the payment form
function initializePaymentForm() {
    var form = document.getElementById('payment-form');

    // Handle form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        handleFormSubmission(form); // Call the function to handle form submission
    });

    // Create an instance of the card Element
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element
    card.addEventListener('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });
}

// Call the function to initialize the payment form when the DOM is loaded
document.addEventListener('DOMContentLoaded', initializePaymentForm);
document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submit-button');

    submitButton.addEventListener('click', function(event) {
        event.preventDefault();

        // Hardcoded card details
        const cardDetails = {
            number: '4242424242424242',
            exp_month: 12,
            exp_year: 2023,
            cvc: '123'
        };

        // Send card details to the server for processing
        sendPaymentDetails(cardDetails);
    });

    // Function to send payment details to the server
    function sendPaymentDetails(cardDetails) {
        // Perform AJAX request to send card details to the server
        // Replace '/payment_method/' with the appropriate endpoint URL
        fetch('/payment_method/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cardDetails)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Payment failed');
            }
        })
        .then(data => {
            // Handle success response from the server
            alert('Payment successful!');
            // Optionally, redirect the user to a success page
            window.location.href = '/success/';
        })
        .catch(error => {
            // Handle error response from the server
            alert('Payment failed: ' + error.message);
        });
    }
});
function handleFormSubmission(form) {
    // Disable the submit button to prevent multiple submissions
    var submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    // Extract the card element from the form
    var cardElement = form.querySelector('#card-element');

    // Create a token from the card element
    var token = null;
    stripe.createToken(cardElement).then(function(result) {
        // If an error occurs during token creation, display the error message
        if (result.error) {
            var errorElement = form.querySelector('#card-errors');
            errorElement.textContent = result.error.message;
            submitButton.disabled = false; // Re-enable the submit button
        } else {
            // If token creation is successful, append the token to the form and submit the form
            token = result.token;
            var tokenInput = document.createElement('input');
            tokenInput.setAttribute('type', 'hidden');
            tokenInput.setAttribute('name', 'stripeToken');
            tokenInput.setAttribute('value', token.id);
            form.appendChild(tokenInput);
            form.submit();
        }
    });
}