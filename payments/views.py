from django.shortcuts import render
from django.http import JsonResponse
import stripe

# Assuming you've already configured your Stripe API keys
stripe.api_key = 'sk_test_51OjyPXSHvzT4MJlEjQZYzE8ZZek9oh7fW6rdyQMjLxpVTPTXfbAVXtvlAjCc1BG6W5oDG2zK21rdazMeeGCURHHD008sz9EMrt'

def add_payment_method(request):
    try:
        customer = stripe.Customer.create(
            name='Anuj Pratap Singh',
            email='anujpratapsingh905@gmail.com',
            description='Regular customer'
        )

        payment_intent = stripe.PaymentIntent.create(
            customer=customer.id,
            amount=3050,
            currency="usd",
            payment_method="pm_card_visa",
            payment_method_types=["card"],
            metadata={"order_id": "6735"},
            confirm=True  # Automatically confirm the payment intent
        )
        
        # Render the payment_form.html template for GET requests
        return render(request, 'productpayment.html', {'payment_intent': payment_intent})
    
    except stripe.error.CardError as e:
        # If the card requires additional authentication, handle it here
        error_code = e.error.code
        if error_code == 'authentication_required':
            error_message = e.error.message
            # You may want to log the error_message for debugging purposes
            return render(request, 'incomplete_3d_secure.html', {'error_message': error_message})
        else:
            # Handle other card errors
            error_message = e.error.message
            return render(request, 'card_error.html', {'error_message': error_message})
    
    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'error': str(e)})
