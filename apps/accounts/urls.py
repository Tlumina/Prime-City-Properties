from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView, SignUpView, LogoutView, DashboardView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Password Change for Logged-In Admin / Staff / Agents
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/dashboard/'
    ), name='password_change'),
    
    # Forgot Password Flow
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/password-reset/complete/'
    ), name='password_reset_confirm'),
    
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
