from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from .forms import TourBookingForm
from .models import TourBooking
from .utils import send_tour_notification_email
from properties.models import Property


class ScheduleTourView(View):
    template_name = 'tours/tour_schedule.html'

    def get(self, request):
        property_id = request.GET.get('property_id')
        initial_data = {}
        selected_property = None

        if property_id:
            try:
                selected_property = Property.objects.get(id=property_id, is_published=True)
                initial_data['property'] = selected_property
            except Property.DoesNotExist:
                pass

        form = TourBookingForm(initial=initial_data)
        return render(request, self.template_name, {
            'form': form,
            'selected_property': selected_property
        })

    def post(self, request):
        form = TourBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            request.session['latest_booking_id'] = booking.id
            messages.success(request, "Your tour request has been successfully submitted! Our private client advisor will call you to confirm.")
            return redirect('tours:success')
        
        return render(request, self.template_name, {'form': form})


class TourSuccessView(View):
    template_name = 'tours/tour_success.html'

    def get(self, request):
        booking_id = request.session.get('latest_booking_id')
        booking = None
        if booking_id:
            try:
                booking = TourBooking.objects.get(id=booking_id)
            except TourBooking.DoesNotExist:
                pass

        return render(request, self.template_name, {'booking': booking})


class StaffTourManageView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'tours/tour_manage.html'
    login_url = '/admin/login/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get(self, request):
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('q', '').strip()

        bookings = TourBooking.objects.select_related('property').all()

        if status_filter:
            bookings = bookings.filter(status=status_filter)

        if search_query:
            bookings = bookings.filter(
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(property__title__icontains=search_query)
            )

        context = {
            'bookings': bookings,
            'status_filter': status_filter,
            'search_query': search_query,
            'stats': {
                'total': TourBooking.objects.count(),
                'pending': TourBooking.objects.filter(status=TourBooking.Status.PENDING).count(),
                'confirmed': TourBooking.objects.filter(status=TourBooking.Status.CONFIRMED).count(),
                'completed': TourBooking.objects.filter(status=TourBooking.Status.COMPLETED).count(),
                'cancelled': TourBooking.objects.filter(status=TourBooking.Status.CANCELLED).count(),
            },
            'status_choices': TourBooking.Status.choices
        }
        return render(request, self.template_name, context)

    def post(self, request):
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        if booking_id and new_status in dict(TourBooking.Status.choices):
            booking = get_object_or_404(TourBooking, id=booking_id)
            old_status = booking.status
            booking.status = new_status
            booking.save()
            if old_status != new_status:
                send_tour_notification_email(booking)
            messages.success(request, f"Tour booking #{booking.id} status updated to '{booking.get_status_display()}' & buyer notified via email.")
        return redirect('tours:manage')
