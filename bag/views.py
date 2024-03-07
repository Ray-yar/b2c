from django.shortcuts import render, redirect
from django.contrib import messages

def view_bag(request):
    return render(request, 'components/bag/bag.html')



def add_to_bag(request, item_id):
    bag = request.session.get('bag', {})
    
    quantity = int(request.POST.get('quantity'))
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    
    messages.success(request, 'Successfully added into the shopping bag!')

    request.session['bag'] = bag
    redirect_url = request.POST.get('redirect_url')
    return redirect(redirect_url)