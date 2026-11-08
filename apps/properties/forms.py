from django import forms
from .models import Location, PropertyType, Property, PropertyFeature


class PropertySearchFilterForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        empty_label="All Locations",
        widget=forms.Select(attrs={'class': 'form-select luxury-select', 'aria-label': 'Select Location'})
    )
    property_type = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(),
        required=False,
        empty_label="All Types",
        widget=forms.Select(attrs={'class': 'form-select luxury-select', 'aria-label': 'Property Type'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + list(Property.Status.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select luxury-select', 'aria-label': 'Property Status'})
    )
    bedrooms = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Min Beds', 'aria-label': 'Bedrooms'})
    )
    bathrooms = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Min Baths', 'aria-label': 'Bathrooms'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Min Price (₦)', 'aria-label': 'Min Price'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Max Price (₦)', 'aria-label': 'Max Price'})
    )
    min_sqm = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Min Size (sqm)', 'aria-label': 'Min Sqm'})
    )
    has_garage = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'filter_garage'})
    )
    has_pool = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'filter_pool'})
    )
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Search by title or keyword...', 'aria-label': 'Keyword Search'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest First'),
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
            ('-size_sqm', 'Largest Size'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={'class': 'form-select luxury-select', 'aria-label': 'Sort By'})
    )


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class PropertyCreateForm(forms.ModelForm):
    primary_image = forms.ImageField(
        required=False,
        label="Primary Cover Photo (Upload from Gallery)",
        help_text="Select main photo from your gallery/device",
        widget=forms.FileInput(attrs={'class': 'form-control luxury-input', 'accept': 'image/*'})
    )
    gallery_images = forms.FileField(
        required=False,
        label="Additional Gallery Photos (Upload Multiple)",
        help_text="Hold Ctrl/Shift to select multiple photos from your gallery",
        widget=MultipleFileInput(attrs={'class': 'form-control luxury-input', 'multiple': True, 'accept': 'image/*'})
    )
    primary_image_url = forms.URLField(
        required=False,
        label="External Primary Image URL (Optional)",
        help_text="Or paste an image URL (e.g. Unsplash) if not uploading from gallery",
        widget=forms.URLInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'https://images.unsplash.com/...'})
    )

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'detailed_story', 'price', 'price_label',
            'property_type', 'status', 'location', 'address', 'landmark_notes',
            'bedrooms', 'bathrooms', 'garage_spaces', 'has_swimming_pool', 'size_sqm', 'features'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. The Royal Sovereign 5-Bedroom Mansion', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 2, 'placeholder': 'Short summary of the property...', 'required': True}),
            'detailed_story': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 4, 'placeholder': 'What makes this property special? (Detailed story)...', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Price in Naira (e.g. 150000000)', 'required': True}),
            'price_label': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. Outright or /year for rent'}),
            'property_type': forms.Select(attrs={'class': 'form-select luxury-select', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-select luxury-select', 'required': True}),
            'location': forms.Select(attrs={'class': 'form-select luxury-select', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Street Address / Estate Name', 'required': True}),
            'landmark_notes': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Nearby landmarks e.g. 3 mins from Admiralty Tollgate'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'min': 0}),
            'garage_spaces': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'min': 0}),
            'has_swimming_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'size_sqm': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Size in sqm e.g. 500'}),
            'features': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
