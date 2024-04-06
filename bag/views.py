from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

# def view_bag(request):
#     return render(request, 'components/bag/bag.html')

def add_to_bag(request, item_id):

    bag = request.session.get('bag', {})
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.title} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.title} to your bag')
    
    request.session['bag'] = bag
    return redirect(redirect_url)

@login_required
def add_to_bag(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added {product.title} to your bag')
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer or reverse('homepage'))

@login_required
def remove_from_bag(request, bag_item_id):
    cart_item = CartItem.objects.get(pk=bag_item_id)
    cart_item.delete()
    messages.success(request, f'Successfully removed from your bag')
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer or reverse('homepage'))

@login_required
def view_bag(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total = 0
        for item in cart_items:
            # Calculate subtotal for each item
            item.subtotal = item.product.price * item.quantity
            # Add subtotal of the current item to total
            total += item.subtotal
    except Cart.DoesNotExist:
        total = 0
        cart_items = []
    return render(request, 'components/bag/bag.html', {'cart_items': cart_items, 'total': total})

@login_required
def update_bag_item_quantity(request, bag_item_id):
    cart_item = CartItem.objects.get(pk=bag_item_id)
    new_quantity = int(request.POST.get(f'quantity_{bag_item_id}'))
    cart_item.quantity = new_quantity
    cart_item.save()
    messages.success(request, f'Quantity successfully updated.')
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer or reverse('homepage'))