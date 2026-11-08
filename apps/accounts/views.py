from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from .forms import SignUpForm, LoginForm
from tours.models import TourBooking
from properties.models import Property
from contact.models import ContactMessage


@method_decorator(sensitive_post_parameters('password', 'confirm_password'), name='dispatch')
class SignUpView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to Prime City Properties, {user.first_name}! Your account has been created.")
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {'form': form})


@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.email}!")
            next_url = request.GET.get('next') or 'accounts:dashboard'
            return redirect(next_url)
        messages.error(request, "Invalid email address or password.")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('core:home')

    def post(self, request):
        return self.get(request)


class DashboardView(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'
    login_url = '/login/'

    def get(self, request):
        user = request.user
        
        # User's booked tours matching email or user
        booked_tours = TourBooking.objects.filter(email=user.email).select_related('property')
        
        # If Agent/Staff/Admin, also fetch properties listed
        my_properties = None
        if user.is_real_estate_agent:
            my_properties = Property.objects.select_related('location', 'property_type').all()[:10]

        context = {
            'user': user,
            'booked_tours': booked_tours,
            'my_properties': my_properties,
            'stats': {
                'tours_count': booked_tours.count(),
                'pending_tours': booked_tours.filter(status=TourBooking.Status.PENDING).count(),
                'confirmed_tours': booked_tours.filter(status=TourBooking.Status.CONFIRMED).count(),
            }
        }
        return render(request, self.template_name, context)
