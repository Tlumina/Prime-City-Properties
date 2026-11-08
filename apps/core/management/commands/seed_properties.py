from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import SiteSetting, Testimonial, LegalPage
from properties.models import Location, PropertyType, PropertyFeature, Property, PropertyImage
from tours.models import TourBooking
from accounts.models import User
import datetime


class Command(BaseCommand):
    help = "Seeds database with realistic Nigerian luxury real estate data for Prime City Properties."

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing Prime City Properties seed data...")

        # 1. Site Settings
        site_setting = SiteSetting.load()
        site_setting.company_name = "Prime City Properties"
        site_setting.tagline = "Stop Searching. Start Living."
        site_setting.phone_number = "+234 803 123 4567"
        site_setting.whatsapp_number = "2348031234567"
        site_setting.email = "info@primecityproperties.ng"
        site_setting.office_address = "Plot 14, Admiralty Way, Lekki Phase 1, Lagos, Nigeria"
        site_setting.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site Settings configured"))

        # 2. Superuser check
        if not User.objects.filter(email='admin@primecityproperties.ng').exists():
            admin_user = User.objects.create_superuser(
                email='admin@primecityproperties.ng',
                password='adminpassword123',
                first_name='Chief',
                last_name='Administrator',
                phone_number='+234 802 000 1122'
            )
            self.stdout.write(self.style.SUCCESS("[OK] Default Admin created (admin@primecityproperties.ng / adminpassword123)"))

        # 3. Legal Pages
        legal_pages = [
            {
                'slug': 'terms',
                'title': 'Terms & Conditions',
                'content': '''<h3>1. Introduction</h3><p>Welcome to Prime City Properties. By accessing or using our real estate services, digital platform, or scheduling property viewings, you agree to comply with and be bound by the following terms and conditions.</p><h3>2. Property Listings & Accuracy</h3><p>While Prime City Properties exercises utmost due diligence to verify property documentation (including Certificate of Ownership, Governor's Consent, and Gazettes), property details, prices, and availability are subject to confirmation at the time of agreement signing.</p><h3>3. Tour Bookings</h3><p>Scheduling a property tour via this platform constitutes an appointment request. Official confirmation will be communicated by a assigned Private Client Advisor.</p>'''
            },
            {
                'slug': 'refund-policy',
                'title': 'Refund Policy',
                'content': '''<h3>1. Booking & Commitment Deposits</h3><p>All property reservation deposits held by Prime City Properties are maintained in a secure escrow account in accordance with Nigerian real estate regulations.</p><h3>2. Inspection Fees</h3><p>Physical tour scheduling through Prime City Properties is complimentary for accredited buyers. Special customized video drone surveys or technical structural audits may incur non-refundable administrative fees as mutually agreed.</p>'''
            },
            {
                'slug': 'privacy-policy',
                'title': 'Privacy Policy',
                'content': '''<h3>1. Data Collection</h3><p>Prime City Properties respects your privacy and complies with the Nigeria Data Protection Regulation (NDPR). We collect personal information (name, telephone number, email address) solely for facilitating property inquiries, tour arrangements, and legal documentation.</p><h3>2. Security Safeguards</h3><p>We utilize enterprise-grade SSL encryption and secure database controls to safeguard client credentials and high-net-worth transactional privacy.</p>'''
            },
            {
                'slug': 'accessibility',
                'title': 'Accessibility Statement',
                'content': '''<h3>Our Commitment</h3><p>Prime City Properties is committed to ensuring digital accessibility for all users, including individuals with disabilities. We continuously optimize our web interface according to WCAG 2.2 AA standards.</p>'''
            }
        ]

        for lp in legal_pages:
            LegalPage.objects.update_or_create(
                slug=lp['slug'],
                defaults={'title': lp['title'], 'content': lp['content']}
            )
        self.stdout.write(self.style.SUCCESS("[OK] Legal pages created"))

        # 4. Property Types
        types_data = [
            {'name': 'Executive Duplex', 'icon_class': 'bi-building-gear', 'desc': 'Standalone & Semi-Detached Luxury Duplexes'},
            {'name': 'Penthouse Suite', 'icon_class': 'bi-building-up', 'desc': 'Ultra-luxurious high-rise skyline residences'},
            {'name': 'Luxury Villa', 'icon_class': 'bi-house-heart', 'desc': 'Spacious waterfront & gated estate mansions'},
            {'name': 'Serviced Apartment', 'icon_class': 'bi-door-open', 'desc': 'Fully furnished short-let and residential apartments'},
            {'name': 'Commercial Hub', 'icon_class': 'bi-briefcase', 'desc': 'Grade-A office suites and prime retail outlets'},
            {'name': 'Residential Land Plot', 'icon_class': 'bi-geo-alt', 'desc': 'Dry land plots with verified C of O titles'},
        ]
        type_objs = {}
        for t in types_data:
            obj, _ = PropertyType.objects.update_or_create(
                slug=slugify(t['name']),
                defaults={'name': t['name'], 'icon_class': t['icon_class'], 'description': t['desc']}
            )
            type_objs[t['name']] = obj

        # 5. Locations
        locations_data = [
            {
                'name': 'Lekki Phase 1', 'city': 'Lagos', 'state': 'Lagos State',
                'desc': 'Prime commercial & luxury residential node in Lagos Coastline',
                'img': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Ikoyi', 'city': 'Lagos', 'state': 'Lagos State',
                'desc': 'Nigeria’s premier affluent district with golf courses & diplomatic quarters',
                'img': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Victoria Island', 'city': 'Lagos', 'state': 'Lagos State',
                'desc': 'Financial heartbeat & upscale high-rise residential district',
                'img': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Banana Island', 'city': 'Lagos', 'state': 'Lagos State',
                'desc': 'Exclusive man-made island sanctuary for high net worth individuals',
                'img': 'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Maitama', 'city': 'Abuja', 'state': 'FCT Abuja',
                'desc': 'Prestige diplomatic zone in Nigeria’s Federal Capital Territory',
                'img': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'GRA Phase 2', 'city': 'Port Harcourt', 'state': 'Rivers State',
                'desc': 'High-end serene residential enclave in the Garden City',
                'img': 'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=800&q=80'
            },
        ]
        location_objs = {}
        for l in locations_data:
            obj, _ = Location.objects.update_or_create(
                slug=slugify(f"{l['name']}-{l['city']}"),
                defaults={
                    'name': l['name'], 'city': l['city'], 'state': l['state'],
                    'description': l['desc'], 'image_url': l['img'], 'is_featured': True
                }
            )
            location_objs[l['name']] = obj

        # 6. Features
        features_list = [
            '24/7 Armed Security & CCTV',
            'Olympic-Size Swimming Pool',
            'Certificate of Occupancy (C of O)',
            'Smart Home Automation',
            'Private Cinema Room',
            'Fully Equipped Gym',
            '24/7 Industrial Generator',
            'Solar Power Inverter System',
            'Private Passenger Elevator',
            'Fitted Chef Kitchen',
            'Water Treatment Plant',
            'Automated Gate System'
        ]
        feat_objs = {}
        for f in features_list:
            obj, _ = PropertyFeature.objects.get_or_create(name=f)
            feat_objs[f] = obj

        # 7. Properties Seed
        properties_data = [
            {
                'title': 'The Sovereign Court 5-Bedroom Fully Detached Mansion',
                'price': 450000000.00,
                'type': 'Luxury Villa',
                'location': 'Banana Island',
                'address': 'Plot 8, Zone A, Banana Island, Ikoyi, Lagos',
                'landmark': 'Near Banana Island Marina',
                'beds': 5, 'baths': 6, 'garage': 4, 'pool': True, 'sqm': 750,
                'status': Property.Status.FOR_SALE,
                'featured': True,
                'desc': 'An architectural masterpiece featuring breathtaking waterfront panoramas, private cinema, rooftop terrace, and smart automation in Nigeria’s safest gated sanctuary.',
                'story': 'Welcome to The Sovereign Court. Designed for executive distinction, this residence seamlessly blends Italian marble flooring with customized mahogany millwork. The double-volume living room cascades into an infinity-edge pool facing the Lagos Lagoon. Comes with complete Governor’s Consent.',
                'images': [
                    'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=1200&q=80',
                ],
                'feats': ['24/7 Armed Security & CCTV', 'Olympic-Size Swimming Pool', 'Certificate of Occupancy (C of O)', 'Smart Home Automation', 'Private Cinema Room', 'Private Passenger Elevator']
            },
            {
                'title': 'Grand Horizon 4-Bedroom Semi-Detached Smart Duplex',
                'price': 185000000.00,
                'type': 'Executive Duplex',
                'location': 'Lekki Phase 1',
                'address': 'Off Admiralty Way, Lekki Phase 1, Lagos',
                'landmark': '3 Minutes from Lekki-Ikoyi Link Bridge',
                'beds': 4, 'baths': 5, 'garage': 3, 'pool': True, 'sqm': 450,
                'status': Property.Status.FOR_SALE,
                'featured': True,
                'desc': 'Brand new contemporary 4-bedroom duplex with BQ, fitted kitchen, swimming pool, and solar hybrid backup power in central Lekki Phase 1.',
                'story': 'Positioned in a serene residential close off Admiralty Way, Grand Horizon offers supreme convenience. Each bedroom features ensuite modern sanitary ware, walk-in closets, and private balcony vistas. Ideal for growing families or discerning investors seeking premium rental yields.',
                'images': [
                    'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',
                ],
                'feats': ['24/7 Armed Security & CCTV', 'Solar Power Inverter System', 'Fitted Chef Kitchen', 'Smart Home Automation', 'Water Treatment Plant']
            },
            {
                'title': 'Skyline Royal Penthouse with Private Rooftop Lounge',
                'price': 650000000.00,
                'type': 'Penthouse Suite',
                'location': 'Ikoyi',
                'address': 'Bouridillon Road, Ikoyi, Lagos',
                'landmark': 'Opposite Ikoyi Golf Club',
                'beds': 4, 'baths': 5, 'garage': 3, 'pool': True, 'sqm': 620,
                'status': Property.Status.FOR_SALE,
                'featured': True,
                'desc': 'Ultra-exclusive triplex penthouse occupying the entire top floor with 360-degree aerial views across Ikoyi, Five Cowries Creek, and the Atlantic Ocean.',
                'story': 'Standing atop Bouridillon Road, Skyline Royal Penthouse sets a new standard for luxury living in West Africa. Features include floor-to-ceiling double glazed acoustic windows, private heated jacuzzi, personal elevator key-code access, and dedicated concierge services.',
                'images': [
                    'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=80',
                ],
                'feats': ['Private Passenger Elevator', 'Olympic-Size Swimming Pool', '24/7 Industrial Generator', 'Private Cinema Room', 'Smart Home Automation']
            },
            {
                'title': 'Diplomatic Crest 5-Bedroom Villa with Swimming Pool',
                'price': 380000000.00,
                'type': 'Luxury Villa',
                'location': 'Maitama',
                'address': 'Transcorp Hilton Axis, Maitama, Abuja FCT',
                'landmark': '5 Mins from Federal Secretariat',
                'beds': 5, 'baths': 6, 'garage': 5, 'pool': True, 'sqm': 800,
                'status': Property.Status.FOR_SALE,
                'featured': True,
                'desc': 'Palatial mansion situated in Abuja’s prestigious Maitama District, complete with 2-room BQ, manicured gardens, and state-of-the-art security perimeter.',
                'story': 'Designed for high-ranking diplomats, executives, and public dignitaries. Diplomatic Crest provides unparalleled privacy behind high fortified perimeter walls, complete with bulletproof doors, centralized climate control, and extensive underground parking.',
                'images': [
                    'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',
                ],
                'feats': ['24/7 Armed Security & CCTV', 'Certificate of Occupancy (C of O)', 'Fully Equipped Gym', '24/7 Industrial Generator', 'Automated Gate System']
            },
            {
                'title': 'The Palms Executive 3-Bedroom Serviced Apartment',
                'price': 25000000.00, # Per Year Rent
                'price_label': '/year',
                'type': 'Serviced Apartment',
                'location': 'Victoria Island',
                'address': 'Ahmadu Bello Way, Victoria Island, Lagos',
                'landmark': 'Adjacent to Eko Hotel & Suites',
                'beds': 3, 'baths': 3, 'garage': 2, 'pool': True, 'sqm': 280,
                'status': Property.Status.FOR_RENT,
                'featured': False,
                'desc': 'Exquisitely furnished 3-bedroom luxury serviced apartment with 24-hour power, facility management, rooftop pool, and ocean views.',
                'story': 'Perfect executive residence in Victoria Island. Enjoy seamless plug-and-play living with daily housekeeping, ultra-fast fiber optics, full kitchen appliances, and 24/7 security guard patrol.',
                'images': [
                    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80',
                ],
                'feats': ['24/7 Industrial Generator', 'Water Treatment Plant', 'Olympic-Size Swimming Pool', 'Fully Equipped Gym']
            },
            {
                'title': 'Garden City Haven 4-Bedroom Detached House',
                'price': 140000000.00,
                'type': 'Executive Duplex',
                'location': 'GRA Phase 2',
                'address': 'Tombia Street, GRA Phase 2, Port Harcourt',
                'landmark': 'Near Hotel Presidential',
                'beds': 4, 'baths': 4, 'garage': 3, 'pool': False, 'sqm': 500,
                'status': Property.Status.FOR_SALE,
                'featured': False,
                'desc': 'Elegant family home nestled in a tranquil tree-lined avenue in Port Harcourt GRA, featuring perimeter security and serene gardens.',
                'story': 'Built to international structural standards with imported granite finishes, overhead water treatment facility, double BQ, and space for a private pool installation.',
                'images': [
                    'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',
                ],
                'feats': ['Certificate of Occupancy (C of O)', '24/7 Armed Security & CCTV', 'Solar Power Inverter System']
            }
        ]

        for pdata in properties_data:
            prop, created = Property.objects.update_or_create(
                slug=slugify(pdata['title']),
                defaults={
                    'title': pdata['title'],
                    'price': pdata['price'],
                    'price_label': pdata.get('price_label', ''),
                    'property_type': type_objs[pdata['type']],
                    'location': location_objs[pdata['location']],
                    'address': pdata['address'],
                    'landmark_notes': pdata['landmark'],
                    'bedrooms': pdata['beds'],
                    'bathrooms': pdata['baths'],
                    'garage_spaces': pdata['garage'],
                    'has_swimming_pool': pdata['pool'],
                    'size_sqm': pdata['sqm'],
                    'status': pdata['status'],
                    'is_featured': pdata['featured'],
                    'is_published': True,
                    'description': pdata['desc'],
                    'detailed_story': pdata['story'],
                }
            )

            # Assign features
            for f_name in pdata['feats']:
                if f_name in feat_objs:
                    prop.features.add(feat_objs[f_name])

            # Images
            prop.images.all().delete()
            for idx, img_url in enumerate(pdata['images']):
                PropertyImage.objects.create(
                    property=prop,
                    image_url=img_url,
                    caption=f"{prop.title} - View {idx + 1}",
                    is_primary=(idx == 0),
                    display_order=idx
                )
        self.stdout.write(self.style.SUCCESS("[OK] Sample properties & images populated"))

        # 8. Testimonials
        testimonials_data = [
            {
                'name': 'Dr. Babatunde Ogunlesi',
                'role': 'Homeowner, Ikoyi Lagos',
                'quote': 'Prime City Properties delivered complete transparency when acquiring our Bouridillon residence. From C of O verification to final title transfer, their professionalism is unmatched.',
                'rating': 5
            },
            {
                'name': 'Chief Mrs. Florence Adeleke',
                'role': 'Property Investor, Abuja',
                'quote': 'Stop Searching. Start Living is not just a slogan—it is their operational reality. They sourced two high-yield penthouses for my portfolio in record time.',
                'rating': 5
            },
            {
                'name': 'Engr. Emeka Nwachukwu',
                'role': 'Resident, Lekki Phase 1',
                'quote': 'Finding a genuine dry land duplex in Lekki with verified documentation can be stressful. Prime City Properties handled every audit seamlessly.',
                'rating': 5
            }
        ]
        for tdata in testimonials_data:
            Testimonial.objects.get_or_create(
                client_name=tdata['name'],
                defaults={'client_role_or_location': tdata['role'], 'quote': tdata['quote'], 'rating': tdata['rating'], 'is_featured': True}
            )
        self.stdout.write(self.style.SUCCESS("[OK] Testimonials created"))

        # 9. Sample Tour Booking
        if Property.objects.exists():
            sample_prop = Property.objects.first()
            TourBooking.objects.get_or_create(
                email='client@example.com',
                defaults={
                    'property': sample_prop,
                    'full_name': 'Alhaji Ibrahim Danjuma',
                    'phone_number': '+234 803 999 8877',
                    'preferred_date': datetime.date.today() + datetime.timedelta(days=3),
                    'preferred_time': '11:00 AM',
                    'message': 'Interested in inspecting the master suite and checking battery inverter specs.',
                    'status': TourBooking.Status.PENDING
                }
            )
        self.stdout.write(self.style.SUCCESS("[OK] Sample tour booking added"))
        self.stdout.write(self.style.SUCCESS("\n[SUCCESS] Prime City Properties database successfully seeded!"))
