from django.test import TestCase
from django.urls import reverse
from .models import Location, PropertyType, Property, PropertyFeature


class PropertyModelAndFilterTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Lekki Phase 1", city="Lagos", state="Lagos State")
        self.prop_type = PropertyType.objects.create(name="Executive Duplex")
        self.feature = PropertyFeature.objects.create(name="Swimming Pool")
        
        self.property = Property.objects.create(
            title="Luxury 4 Bedroom Duplex",
            price=150000000.00,
            property_type=self.prop_type,
            location=self.location,
            address="Admiralty Way, Lekki",
            bedrooms=4,
            bathrooms=4,
            garage_spaces=2,
            has_swimming_pool=True,
            size_sqm=450,
            status=Property.Status.FOR_SALE,
            is_featured=True,
            is_published=True,
            description="Beautiful modern duplex in Lekki",
            detailed_story="Detailed story of the duplex"
        )

    def test_property_slug_and_formatted_price(self):
        self.assertEqual(self.property.slug, "luxury-4-bedroom-duplex")
        self.assertEqual(self.property.formatted_price, "₦150,000,000")

    def test_property_list_view(self):
        response = self.client.get(reverse('properties:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Luxury 4 Bedroom Duplex")

    def test_property_filter_by_location(self):
        response = self.client.get(reverse('properties:list') + f"?location={self.location.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Luxury 4 Bedroom Duplex")

    def test_property_detail_view(self):
        response = self.client.get(self.property.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Luxury 4 Bedroom Duplex")

    def test_property_creation_by_agent(self):
        from django.contrib.auth import get_user_model
        from django.core.files.uploadedfile import SimpleUploadedFile
        User = get_user_model()

        agent = User.objects.create_user(
            email='agent@primecity.ng',
            password='Password123!',
            role=User.Role.AGENT,
            first_name='Agent',
            last_name='User'
        )
        self.client.force_login(agent)

        dummy_image = SimpleUploadedFile(
            name='test_house.gif',
            content=b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
            content_type='image/gif'
        )

        response = self.client.post(reverse('properties:create'), {
            'title': 'Ikoyi Penthouse Suite',
            'property_type': self.prop_type.id,
            'price': '450000000',
            'price_label': 'Outright',
            'status': Property.Status.FOR_SALE,
            'description': 'Stunning penthouse suite in Ikoyi',
            'detailed_story': 'Detailed story of Ikoyi Penthouse',
            'location': self.location.id,
            'address': 'Bourdillon Road, Ikoyi',
            'bedrooms': 5,
            'bathrooms': 5,
            'garage_spaces': 3,
            'size_sqm': '600',
            'has_swimming_pool': False,
            'primary_image': dummy_image
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Property.objects.filter(title='Ikoyi Penthouse Suite').exists())
        new_prop = Property.objects.get(title='Ikoyi Penthouse Suite')
        self.assertTrue(new_prop.images.exists())
