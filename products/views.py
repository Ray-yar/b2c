from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Review
from .forms import ReviewForm, ContactForm

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
        
    if request.method == 'POST':
        review_id = request.POST.get('id')
        if review_id:
            # Editing an existing review
            review = get_object_or_404(Review, id=review_id)
            review_form = ReviewForm(request.POST, instance=review)
            messages.success(request, "Review updated successfully.")
        else:
            # Inserting a new review
            review_form = ReviewForm(request.POST)
            messages.success(request, "Review inserted successfully, please wait we will publish it after a quick review.")

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.prod = product
            review.user = request.user
            review.save()
            review_form = ReviewForm()
        else:
            review = None

        return redirect('/products/'+product_id+'/')
    else: 
        reviews = Review.objects.filter(prod=product, approved=True)
        context = {
            'product': product,
            'reviews' : reviews,
            'review_form' : ReviewForm()
        }
        return render(request, 'product_details.html', context)

def delete_review(request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if not request.user.is_authenticated or review.user != request.user:
            messages.error(request, "You don't have permission to delete this review.")
            return HttpResponseBadRequest("You don't have permission to delete this review.")
        else:
            review.delete()
            messages.success(request, "Review deleted successfully.")
            return HttpResponse("Review deleted successfully.", status=200)

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
            {
                'page_title': "Contact Us"
            }
        )
    

