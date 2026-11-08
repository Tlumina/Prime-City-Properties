from django import forms
from django.utils import timezone
from .models import TourBooking
from properties.models import Property


class TourBookingForm(forms.ModelForm):
    property = forms.ModelChoiceField(
        queryset=Property.objects.filter(is_published=True),
        required=False,
        empty_label="Select Property (Optional)",
        widget=forms.Select(attrs={'class': 'form-select luxury-select', 'aria-label': 'Select Property'})
    )

    class Meta:
        model = TourBooking
        fields = ['property', 'full_name', 'email', 'phone_number', 'preferred_date', 'preferred_time', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Phone (e.g. +234 806 854 2996)', 'required': True}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control luxury-input', 'type': 'date', 'required': True}),
            'preferred_time': forms.Select(attrs={'class': 'form-select luxury-select', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 3, 'placeholder': 'Any specific requirements or questions? (Optional)'}),
        }

    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("Please select a current or future date for your tour.")
        return date

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if len(phone) < 8:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
