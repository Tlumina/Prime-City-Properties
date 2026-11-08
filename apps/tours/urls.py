from django.urls import path
from .views import ScheduleTourView, TourSuccessView, StaffTourManageView

app_name = 'tours'

urlpatterns = [
    path('', ScheduleTourView.as_view(), name='schedule'),
    path('success/', TourSuccessView.as_view(), name='success'),
    path('manage/', StaffTourManageView.as_view(), name='manage'),
]
