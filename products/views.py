from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib import messages


class ProductsView(View):
    template_name = "index.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
