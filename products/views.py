from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views import generic, View
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review, Wishlist
from .forms import ReviewForm, ContactForm, WishlistForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

class ProductView(generic.ListView):
    model = Product
    template_name = "index.html"
    paginate_by = 8

    def get_queryset(self):
        products = super().get_queryset()
        selected_query = self.request.GET.get('q')
        selected_category = self.request.GET.get('category')
        
        if selected_category:
            products = products.filter(category=selected_category)
        if selected_query:
            queries = Q(title__icontains=selected_query) | Q(desc__icontains=selected_query)
            products = products.filter(queries)
        
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wish_list_form'] = WishlistForm()
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        if self.request.GET.get('q'):
            context['selected_query'] = self.request.GET.get('q')
        else:
            context['selected_query'] = ''
        context['products_page'] = True
        return context


def home(request):
    products = Product.objects.all()[:6]
    categories = Category.objects.all()[:17]
    selected_query = ''
    selected_category = None
    context = {
        'wish_list_form': WishlistForm(),
        'product_list': products,
        "categories": categories,
    }
    return render(request, 'home.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, product.title + " added to your wishlist.")
    
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer or reverse('homepage'))
    
@login_required
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    messages.success(request, product.title + " removed from your wishlist.")

    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer or reverse('homepage'))

@login_required
def wishlist(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        products = wishlist.products.all()
    except Wishlist.DoesNotExist:
        products = []
    
    return render(request, 'wish_list.html', {'product_list': products, 'remove_wishlist': True})

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
            return HttpResponse("You don't have permission to delete this review.")
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
                'contact_form' : ContactForm(),
                'page_title': "Contact Us"
            },
        )
    

def about_us(request):
       return render(
            request,
            'about_us.html', 
            {
                'page_title': "About Us"
            }
        )
    

