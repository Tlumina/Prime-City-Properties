from django.urls import path
from .views import HomeView, AboutView, LegalPageView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('legal/<slug:slug>/', LegalPageView.as_view(), name='legal'),
    
    # Direct short routes for explicit legal URLs
    path('terms/', LegalPageView.as_view(), {'slug': 'terms'}, name='terms'),
    path('refund-policy/', LegalPageView.as_view(), {'slug': 'refund-policy'}, name='refund_policy'),
    path('privacy-policy/', LegalPageView.as_view(), {'slug': 'privacy-policy'}, name='privacy_policy'),
    path('accessibility/', LegalPageView.as_view(), {'slug': 'accessibility'}, name='accessibility'),
]
