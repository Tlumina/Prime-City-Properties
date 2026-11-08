from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTestCase(TestCase):
    def test_signup_multiple_users_no_username_integrity_error(self):
        """Verify multiple user signups do not trigger UNIQUE constraint error on username."""
        # User 1 signup
        response1 = self.client.post(reverse('accounts:signup'), {
            'first_name': 'Chidi',
            'last_name': 'Okafor',
            'email': 'chidi@example.com',
            'phone_number': '+2348011111111',
            'role': User.Role.CUSTOMER,
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })
        self.assertEqual(response1.status_code, 302)
        self.assertTrue(User.objects.filter(email='chidi@example.com').exists())
        user1 = User.objects.get(email='chidi@example.com')
        self.assertEqual(user1.username, 'chidi@example.com')

        # User 2 signup (should succeed without IntegrityError)
        response2 = self.client.post(reverse('accounts:signup'), {
            'first_name': 'Amina',
            'last_name': 'Yusuf',
            'email': 'amina@example.com',
            'phone_number': '+2348022222222',
            'role': User.Role.AGENT,
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })
        self.assertEqual(response2.status_code, 302)
        self.assertTrue(User.objects.filter(email='amina@example.com').exists())
        user2 = User.objects.get(email='amina@example.com')
        self.assertEqual(user2.username, 'amina@example.com')
