from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Category(models.Model):
    title = models.CharField(max_length=128, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=128, blank=False)
    desc = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=2)
    featured_photo = CloudinaryField('image', default='placeholder')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title}"   

class Contact(models.Model):
    subject = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    text = models.TextField()
    
    def __str__(self):
        return self.subject