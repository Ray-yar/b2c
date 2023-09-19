from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    
    products = Product.objects.all()
    query = None
    categories = None

    # if request.GET:
    #     if 'category' in request.GET:
    #         categories = request.GET['category'].split(',')
    #         products = products.filter(category__title__in=categories)
    #         categories = Category.objects.filter(title__in=categories)

    #     if 'q' in request.GET:
    #         query = request.GET['q']
    #         if not query:
    #             messages.error(request, "You didn't enter any search criteria!")
    #             return redirect(reverse(''))
            
    #         queries = Q(title__icontains=query) | Q(desc__icontains=query)
    #         products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'categories': categories,
    }
    return render(request, 'index.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'product_details.html', context)
