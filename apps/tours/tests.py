from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import TourBooking


class TourBookingTest(TestCase):
    def test_schedule_tour_post_valid(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        data = {
            'full_name': 'Adeshina Olumide',
            'email': 'adeshina@example.com',
            'phone_number': '+234 803 111 2233',
            'preferred_date': tomorrow.strftime('%Y-%m-%d'),
            'preferred_time': '11:00 AM',
            'message': 'Looking forward to viewing.'
        }
        response = self.client.post(reverse('tours:schedule'), data)
        self.assertEqual(response.status_code, 302) # Redirect to success
        self.assertTrue(TourBooking.objects.filter(email='adeshina@example.com').exists())

    def test_schedule_tour_past_date_invalid(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = {
            'full_name': 'Adeshina Olumide',
            'email': 'adeshina@example.com',
            'phone_number': '+234 803 111 2233',
            'preferred_date': yesterday.strftime('%Y-%m-%d'),
            'preferred_time': '11:00 AM'
        }
        response = self.client.post(reverse('tours:schedule'), data)
        self.assertEqual(response.status_code, 200) # Form re-renders with error
        self.assertFormError(response.context['form'], 'preferred_date', 'Please select a current or future date for your tour.')
