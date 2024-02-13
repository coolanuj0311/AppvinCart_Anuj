import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]  # Increment cartItems instead of assigning
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'imageURL': product.imageURL,
                    'price': product.price,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            if not product.digital:  # Simplified condition for readability
                order['shipping'] = True
        except Product.DoesNotExist:  # Handle product not found exception
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  # Consider adding parentheses for function call
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print('User is not logged in')
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        defaults={'name': name}  # Provide default values using defaults parameter
    )
    if not created:  # Update name if customer exists
        customer.name = name
        customer.save()

    order = Order.objects.create(
        customer=customer,  # Correct the typo 'cutomer' to 'customer'
        complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(  # Use 'OrderItem.objects.create' instead of 'OrderItem.object.create'
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order  # Return customer and order
