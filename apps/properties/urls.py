from django.urls import path
from .views import PropertyListView, PropertyDetailView, PropertyCreateView

app_name = 'properties'

urlpatterns = [
    path('', PropertyListView.as_view(), name='list'),
    path('create/', PropertyCreateView.as_view(), name='create'),
    path('<slug:slug>/', PropertyDetailView.as_view(), name='detail'),
]
