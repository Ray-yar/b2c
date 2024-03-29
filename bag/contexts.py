from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    
    for pro_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=pro_id)
        total += quantity * product.price
        product_count += quantity
        bag_items.append({
            'pro_id': pro_id,
            'quantity': quantity,
            'product': product,
            'subtotal': quantity * product.price
        })
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }

    return context