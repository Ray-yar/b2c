from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    
    products = Product.objects.all()
    selected_query = None
    selected_category = None
    categories = Category.objects.all()

    if request.GET:
        if 'category' in request.GET or 'q' in request.GET:
            selected_query = request.GET['q']
            selected_category = request.GET['category']
            if selected_category:
                products = products.filter(id=selected_category)
            if selected_query:
                queries = Q(title__icontains=selected_query) | Q(desc__icontains=selected_query)
                products = products.filter(queries)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_query': selected_query
    }
    return render(request, 'index.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'product_details.html', context)
