from django.db import models
from properties.models import Property


class TourBooking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Confirmation'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    TIME_SLOTS = [
        ('09:00 AM', '09:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('01:00 PM', '01:00 PM'),
        ('03:00 PM', '03:00 PM'),
        ('05:00 PM', '05:00 PM'),
    ]

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='tour_bookings')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, help_text="e.g. +234 806 854 2996")
    preferred_date = models.DateField(help_text="Requested date for property walk-through")
    preferred_time = models.CharField(max_length=20, choices=TIME_SLOTS, default='11:00 AM')
    message = models.TextField(blank=True, null=True, help_text="Special requests or specific questions")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tour Booking"
        verbose_name_plural = "Tour Bookings"

    def __str__(self):
        prop_title = self.property.title if self.property else "General Advisory Tour"
        return f"{self.full_name} - {prop_title} ({self.preferred_date})"
