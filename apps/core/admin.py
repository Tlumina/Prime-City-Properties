from django.contrib import admin
from .models import SiteSetting, Testimonial, LegalPage


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'email', 'office_address')
    
    def has_add_permission(self, request):
        # Don't allow adding more than 1 setting instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role_or_location', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'rating', 'created_at')
    search_fields = ('client_name', 'quote', 'client_role_or_location')


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
