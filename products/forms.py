from django import forms
from .models import Contact, Review

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('subject', 'email', 'text',)
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'text',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }

class WishlistForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

