from django.contrib import admin
from .models import Product, Review, Contact, Category
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('title',)
    search_fields = ['title',]
    list_display = ('title',)

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_filter = ('title',)
    search_fields = ['title', 'desc']
    list_display = ('title', 'price', 'created_at')
    summernote_fields = ('desc')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('title',)
    search_fields = ['title',]
    list_display = ('title', 'approved')
    summernote_fields = ('text')
    actions = ['approve_review']

    def approve_review(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter = ('subject',)
    search_fields = ['subject',]
    list_display = ('subject',)
    summernote_fields = ('text')