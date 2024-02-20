from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
import stripe
import stripe
from django.shortcuts import render
from django.http import HttpResponse


# Assuming you've already configured your Stripe API keys
stripe.api_key = 'sk_test_51OjyPXSHvzT4MJlEjQZYzE8ZZek9oh7fW6rdyQMjLxpVTPTXfbAVXtvlAjCc1BG6W5oDG2zK21rdazMeeGCURHHD008sz9EMrt'

def payment_method(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')
        
        try:
            # Create a new customer in Stripe
            customer = stripe.Customer.create(
            payment_method=payment_method_id,
            email=request.user.email,  # Assuming you have a user object
            invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
            
            # Optionally, save the payment method ID to your user's profile
            # request.user.payment_method_id = payment_method_id
            # request.user.save()

            # Send email notification
            send_mail(
                'Payment Successful',
                'Your payment was successful.',
                'apshvp@gmail.com',  # Replace with sender email
                ['lavashri0303@gmail.com'],  # Replace with recipient email
                fail_silently=False,
            )


            # Render payment.html template with success message
            return render(request, 'productpayment.html', {'success': True})
        except stripe.error.InvalidRequestError as e:
            # Return error response if the payment method ID is invalid
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Return error response for other exceptions
            return JsonResponse({'error': str(e)}, status=500)
    else:
        payment_intent = stripe.PaymentIntent.create(
               # Adjust amount as needed (in cents)
           
            amount=3050,  # Adjust amount as needed (in cents)
            currency="usd",
            payment_method_types=["card"],
            metadata={"order_id": "6735"}
        )
     
        # Render the payment_form.html template for GET requests
        return render(request, 'productpayment.html',{'payment_intent': payment_intent})
    
    
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
import stripe
from django.views.decorators.csrf import csrf_exempt
from accounted.models import User
from store.models import Order,Product # Adjusted import for models
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def CheckoutView(request):
    
    # @csrf_exempt
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
    
    # def get(self, request,*args,**kwargs):
    #     user_id = kwargs.get('user_id')
    #     user = User.objects.get(id=user_id)
    #     order_ids = request.GET.getlist('order_ids[]') 
    #     orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
    #     total_amount = 0
    #     for order_id in order_ids:
    #         order = Order.objects.get(pk=order_id)
    #         products = order.product_set.all()  # Changed to product_set
    #         order_amount = sum(product.price for product in products)
    #         total_amount += order_amount
    #     context = {
    #             'user': user,
    #             'orders': orders,
    #             'total_amount': total_amount,
    #         }
    #     request.session['order_ids'] = order_ids
        return render(request, 'process_checkout.html')

    # def post(self, request,*args,**kwargs):
    #     user_id = kwargs.get('user_id')
    #     user = User.objects.get(id=user_id)
    #     order_ids = request.session.get('order_ids', [])
    #     payment_method_id = request.POST.get('paymentMethodId')
    #     currency = 'usd'
    #     shipping_name = request.POST.get('shippingName')  # Retrieve shipping name from request
    #     shipping_address = request.POST.get('shippingAddress')
    #     shipping_city = request.POST.get('shippingCity')
    #     shipping_country = request.POST.get('shippingCountry')
    #     shipping_state = request.POST.get('shippingState')

    #     try:
    #         total_amount = 0 
    #         payment_intent_items = []

    #         # Iterate over order IDs
    #         for order_id in order_ids:
    #             order = Order.objects.get(pk=order_id)
    #             products = order.product_set.all()  # Changed to product_set
    #             # Calculate total amount for the order
    #             order_amount = sum(product.price for product in products)
    #             total_amount += order_amount  # Add order amount to total amount
    #             # Create payment intent items for each product in the order
    #             for product in products:
    #                 payment_intent_items.append({
    #                     'amount': product.price * 100,  # Amount in cents
    #                     'currency': currency,
    #                     'description': product.name,
    #                     'quantity': 1, 
    #                 })
    #         print(payment_intent_items)
    #         # Create or retrieve a customer in Stripe
    #         customer = stripe.Customer.create(
    #             name=user.name,
    #             email=user.email,
    #         )
            
    #         # Attach the PaymentMethod to the customer
    #         stripe.PaymentMethod.attach(
    #             payment_method_id,
    #             customer=customer.id
    #         )
            
    #         # Modify the billing details of the PaymentMethod
    #         stripe.PaymentMethod.modify(
    #             payment_method_id,
    #             billing_details={
    #                 'name': shipping_name,
    #                 'address': {
    #                     'line1': shipping_address,
    #                     "city": shipping_city,
    #                     "country": shipping_country,
    #                     "state": shipping_state
    #                 }
    #             }
    #         )
            
    #         # Now you can use the total amount to create the PaymentIntent
    #         payment_intent = stripe.PaymentIntent.create(
    #             amount=int(float(total_amount) * 100),
    #             currency=currency,
    #             customer=customer.id,
    #             payment_method=payment_method_id,
    #             description=f"Payment for multiple orders: {payment_method_id}",
    #             # automatic_payment_methods={"enabled": True},
    #             metadata={'order_ids': str(order_ids)},
    #         )

    #         #Update is_paid field for corresponding payment
    #         payment = Payment.objects.create(user=user, amount_paid=total_amount, client_secret=payment_intent.client_secret)
    #         payment.save()
    #         client_secret = payment_intent.client_secret
    #         request.session['order_ids'] = order_ids
    #         request.session['client_secret'] = payment_intent.client_secret
    #         request.session['payment_id'] = payment.id
    #         # return JsonResponse({'client_secret': client_secret}, status=200)
    #         return redirect('pay_for_checkout', user_id=user_id)
    #     except Order.DoesNotExist:
    #         return JsonResponse({'error': 'Order not found'}, status=404)
    #     except stripe.error.StripeError as e:
    #         return JsonResponse({'error': str(e)}, status=500)
        

def PayForCheckoutView(request):
    # @csrf_exempt
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def get(self, request,*args,**kwargs):
    #     client_secret = request.session.get('client_secret','')
    #     payment_id = request.session.get('payment_id',0)
    #     user_id = kwargs.get('user_id')
    #     user = User.objects.get(id=user_id)
    #     orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
    #     order_ids = request.session.get('order_ids', [])
    #     orders = Order.objects.filter(id__in=order_ids)
    #     print('********************************')
    #     print(orders)
    #     print(client_secret)
    #     total_amount = 0
    #     for order_id in order_ids:
    #             order = Order.objects.get(pk=order_id)
    #             products = order.product_set.all()
    #             # Calculate total amount for the order
    #             order_amount = sum(product.price for product in products)
    #             total_amount += order_amount
    #     context = {
    #         'client_secret': client_secret,
    #         'user': user,
    #         'orders': orders,
    #         'total_amount': total_amount,
    #         'payment_id': payment_id
    #     }
        return render(request, 'payment_page.html') 

class PaymentSuccessView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get('payment_id')
        payment = get_object_or_404(Payment, pk=payment_id)
        payment.is_paid = True
        payment.save()
        return render(request, 'payment_success.html')

# class PaymentCancelledView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'payment_cancel.html')

    