from django.test import TestCase
from django.urls import reverse
from .models import ContactMessage


class ContactFormTest(TestCase):
    def test_contact_submission(self):
        data = {
            'name': 'Chidi Kenneth',
            'email': 'chidi@example.com',
            'phone_number': '+234 802 333 4455',
            'subject': 'Inquiry about Lekki Mansion',
            'message': 'Is this property still available for sale?'
        }
        response = self.client.post(reverse('contact:index'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='chidi@example.com').exists())
