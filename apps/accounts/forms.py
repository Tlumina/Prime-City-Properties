from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Create Password (min 8 characters)'}),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Confirm Password'})
    )
    role = forms.ChoiceField(
        choices=[
            (User.Role.CUSTOMER, 'Customer / Buyer (Looking to Buy or Rent)'),
            (User.Role.AGENT, 'Real Estate Agent (Want to List Properties)'),
        ],
        widget=forms.Select(attrs={'class': 'form-select luxury-select'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Phone Number (e.g. +234 806 854 2996)'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email', '').lower().strip()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Password'})
    )
