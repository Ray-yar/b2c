from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Product


class ProductsView(generic.ListView):
    template_name = "index.html"

    model = Product
    object = Product.objects.order_by('created_at')
    paginate_by = 8

