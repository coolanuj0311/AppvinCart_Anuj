from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart
from .utils import cartData
from .utils import guestOrder
import json

from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from store.models import Product

 # Add this import statement
from .models import Product, Order, OrderItem
from .utils import cartData, guestOrder


# Your other views and functions go here
from django.shortcuts import render
from django.views.generic import ListView  # Add this import statement
from .models import Product, Order, OrderItem

def store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def profile(request):
    return render(request, 'profile.html')

from django.shortcuts import render
from .models import Order

def my_orders(request):
    # Get orders associated with the logged-in user
    orders = Order.objects.filter(customer=request.user.customer, complete=True)
    context = {'orders': orders}
    return render(request, 'my_orders.html', context)


 
def cart(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


@csrf_exempt

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            return JsonResponse('Payment complete!', safe=False)
    else:
            customer,order=guestOrder(request,data)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_items:
                order.complete = True
            order.save()
            if order.shipping:
                shipping_data = data.get('shipping')
                if shipping_data:
                    ShippingAddress.objects.create(
                        customer=customer,
                        order=order,
                        address=shipping_data.get('address'),
                        city=shipping_data.get('city'),
                        state=shipping_data.get('state'),
                        pincode=shipping_data.get('pincode')
                    )
            return JsonResponse({'error': 'User is not authenticated'}, status=401)
    
def new_arrivals(request):
    new_arrivals = Product.objects.filter(digital=True)
    return render(request, 'new_arrivals.html', {'new_arrivals': new_arrivals})

class StoreView(ListView):
    model = Product
    template_name = 'store.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_option = self.request.GET.get('sort')

        if sort_option == 'high_to_low':
            queryset = queryset.order_by('-price')
        elif sort_option == 'low_to_high':
            queryset = queryset.order_by('price')

        return queryset

def updateItem(request):
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')

    try:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # Ensure that only the specific product is bought when 'buy' action is received
        if action == 'buy':
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderItem.quantity = 1  # Set quantity to 1 for 'buy now'
            orderItem.save()
            order.save()  # Save the order
            return JsonResponse('Item was bought!', safe=False)

        # For 'add' or 'remove' actions
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()

        return JsonResponse('Item was updated!', safe=False)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
