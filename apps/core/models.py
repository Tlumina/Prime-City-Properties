from django.db import models


class SiteSetting(models.Model):
    company_name = models.CharField(max_length=150, default="Prime City Properties")
    tagline = models.CharField(max_length=255, default="Stop Searching. Start Living.")
    phone_number = models.CharField(max_length=50, default="+234 806 854 2996")
    whatsapp_number = models.CharField(max_length=50, default="2348068542996", help_text="International format without + or spaces e.g. 2348068542996")
    email = models.EmailField(default="info@primecityproperties.ng")
    office_address = models.TextField(default="Plot 14, Admiralty Way, Lekki Phase 1, Lagos, Nigeria")
    business_hours = models.CharField(max_length=200, default="Mon - Sat: 8:00 AM - 6:00 PM | Sun: By Appointment")
    facebook_url = models.URLField(blank=True, default="https://facebook.com/primecityproperties")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/primecityproperties")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/company/primecityproperties")
    twitter_url = models.URLField(blank=True, default="https://twitter.com/primecityprop")
    hero_headline = models.CharField(max_length=255, default="Stop Searching. Start Living.")
    hero_subheadline = models.TextField(default="Discover premier luxury residential homes, executive penthouses, and commercial real estate across Lekki, Ikoyi, Victoria Island, and Abuja.")
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        # Enforce single instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role_or_location = models.CharField(max_length=150, help_text="e.g. Homeowner, Lekki Phase 1")
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.client_role_or_location}"


class LegalPage(models.Model):
    slug = models.SlugField(unique=True, max_length=100, help_text="Page URL slug e.g. terms, privacy-policy, refund-policy, accessibility")
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="HTML formatted content")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Legal Page"
        verbose_name_plural = "Legal Pages"

    def __str__(self):
        return self.title
