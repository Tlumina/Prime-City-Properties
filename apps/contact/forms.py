from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Phone Number (e.g. +234 806 854 2996)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Subject / Property of Interest'}),
            'message': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 5, 'placeholder': 'How can we assist you today?', 'required': True}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please provide your full name.")
        return name
