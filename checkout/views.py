from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.models import Cart
from bag.contexts import bag_contents
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import stripe

@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    # Security - 1. Check Secret Key
    if not stripe_secret_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')
        referer = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer or reverse('homepage'))
    
    stripe.api_key = stripe_secret_key

    # Security - 2. Check Public Key
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')
        referer = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer or reverse('homepage'))

    # Security - 3. Check if products are in bag
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        messages.error(request, "There's nothing in your bag at the moment")
        referer = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer or reverse('homepage'))


    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()
            for cart_item in cart_items:
                try:
                    order_line_item = OrderLineItem(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                    )
                    order_line_item.save()
                except cart_item.product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    
    stripe_total = round(total * 100)
    order_form = OrderForm()
    intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    template = 'components/checkout/checkout.html'
    context = {
        'client_secret': intent.client_secret,
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'bag_items': cart_items,
        'total': total,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.success(request, f'Order successfully processed! Your order number is {order_number}.')

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        cart_items.delete()
        cart.delete()
    except Cart.DoesNotExist:
        pass

    template = 'components/checkout/checkout_success.html'
    return render(request, template, {'order': order})