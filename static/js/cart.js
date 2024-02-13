// Define the function to handle the click event
function handleUpdateCartClick(event) {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log('productId:', productId, 'Action:', action);
    console.log('USER:', user); // Make sure user is defined

    if (user === "AnonymousUser") {
        addCookieItem(productId, action);
    } else {
        updateUserOrder(productId, action);
    }
}

// Attach event listeners to update buttons


var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        if (user === 'AnonymousUser') {
            console.log('User is not authenticated. Redirecting to login page.');
            window.location.href = '/login/';
        } else {
            if (action === 'buy') {
                // Redirect to checkout page after adding the product to the cart
                updateUserOrder(productId, 'add', true);
            } else {
                updateUserOrder(productId, action, false);
            }
        }
    });
}

function updateUserOrder(productId, action, redirectToCheckout) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        if (redirectToCheckout) {
            window.location.href = '/checkout/';
        } else {
            location.reload();
        }
    });
}




// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function addCookieItem(productId,action){
    console.log('Not logged in')
    if(action=='add'){
        if(cart[productId]==undefined){
            cart[productId]={'quantity':1}
        }
        else{
            cart[productId]['quantity']+=1
        }
    }
    if(action=='remove'){
        cart[productId]['quantity']-=1
        if(cart[productId]['quantity']<=0){
            console.log('Item should be deleted')
            delete cart[productId];
        }
        
    }
    console.Log('Cart',cart)
    document.cookie='cart='+JSON.stringify(cart)+";domain;path=/"
    location.reload()
    


}