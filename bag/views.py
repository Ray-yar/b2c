from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    return render(request, 'components/bag/bag.html')

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