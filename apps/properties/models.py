from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=150, help_text="e.g. Lekki Phase 1, Ikoyi, Maitama")
    city = models.CharField(max_length=100, default="Lagos", help_text="e.g. Lagos, Abuja, Port Harcourt")
    state = models.CharField(max_length=100, default="Lagos State")
    slug = models.SlugField(unique=True, max_length=150)
    image = models.ImageField(upload_to='locations/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="External image CDN URL for seed data")
    is_featured = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.name}, {self.city}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=800&q=80"


class PropertyType(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Luxury Villa, Executive Duplex, Penthouse, Land")
    slug = models.SlugField(unique=True, max_length=100)
    icon_class = models.CharField(max_length=50, default="bi-house-door", help_text="Bootstrap icon name e.g. bi-building")
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Property Types"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PropertyFeature(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. 24/7 Security, Swimming Pool, C of O, Smart Home Technology")
    icon_class = models.CharField(max_length=50, default="bi-check-circle", help_text="Bootstrap icon name")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Property(models.Model):
    class Status(models.TextChoices):
        FOR_SALE = 'FOR_SALE', 'For Sale'
        FOR_RENT = 'FOR_RENT', 'For Rent'
        SOLD = 'SOLD', 'Sold'
        RENTED = 'RENTED', 'Rented'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(help_text="Short summary of the property")
    detailed_story = models.TextField(help_text="In-depth property story / 'What makes this property special?'")
    price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Price in Nigerian Naira (₦)")
    price_label = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. /year for rentals or Outright for sale")
    
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FOR_SALE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='properties')
    address = models.CharField(max_length=255, help_text="Specific street address or estate name")
    landmark_notes = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. 5 mins drive from Chevron Tollgate")
    
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    garage_spaces = models.PositiveIntegerField(default=0)
    has_swimming_pool = models.BooleanField(default=False)
    size_sqm = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total area size in square meters")
    
    features = models.ManyToManyField(PropertyFeature, blank=True, related_name='properties')
    
    is_featured = models.BooleanField(default=False, db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)
    views_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Properties"
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['status']),
            models.Index(fields=['bedrooms']),
            models.Index(fields=['is_published', 'is_featured']),
        ]

    def __str__(self):
        return f"{self.title} - ₦{self.price:,.2f}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})

    @property
    def formatted_price(self):
        return f"₦{self.price:,.0f}"

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        if img:
            return img.get_image_url()
        return "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="External high-res image URL for seed data")
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"Image for {self.property.title}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80"
