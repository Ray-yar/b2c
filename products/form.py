from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('subject', 'email', 'text',)
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }