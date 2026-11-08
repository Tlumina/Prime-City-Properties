from django.contrib import admin
from .models import TourBooking
from .utils import send_tour_notification_email


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'property', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'preferred_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'property__title')
    ordering = ('-created_at',)
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        send_tour_notification_email(obj)

    @admin.action(description="Confirm selected tour bookings & Notify Buyers")
    def mark_confirmed(self, request, queryset):
        for booking in queryset:
            booking.status = TourBooking.Status.CONFIRMED
            booking.save()
            send_tour_notification_email(booking)

    @admin.action(description="Mark selected tours as COMPLETED & Notify Buyers")
    def mark_completed(self, request, queryset):
        for booking in queryset:
            booking.status = TourBooking.Status.COMPLETED
            booking.save()
            send_tour_notification_email(booking)

    @admin.action(description="Cancel selected tour bookings & Notify Buyers")
    def mark_cancelled(self, request, queryset):
        for booking in queryset:
            booking.status = TourBooking.Status.CANCELLED
            booking.save()
            send_tour_notification_email(booking)
