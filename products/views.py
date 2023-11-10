from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .form import ContactForm

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
                products = products.filter(category=selected_category)
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

def contact_us(request):
    if request.method == 'POST':
        contact_from = ContactForm(request.POST)
        if contact_from.is_valid():
            contact_from.save()
            messages.success(request, "Your Message inserted successfully, thank you for your feedback!")
        else:
            messages.error(request, "Something went wrong! Please try again.")
        return redirect('/contact-us/')
    else:
        return render(
            request, 
            'contact_us.html', 
            {
                'contact_form' : ContactForm()
            },
        )
    

def about_us(request):
       return render(
            request, 
            'about_us.html', 
        )
    

