from django.contrib import admin
from .models import Location, PropertyType, PropertyFeature, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ('image', 'image_url', 'caption', 'is_primary', 'display_order')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'is_featured', 'slug')
    list_filter = ('city', 'state', 'is_featured')
    search_fields = ('name', 'city', 'state')
    prepopulated_fields = {'slug': ('name', 'city')}


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'formatted_price', 'location', 'property_type', 'status', 'bedrooms', 'bathrooms', 'is_featured', 'is_published', 'created_at')
    list_filter = ('status', 'property_type', 'location', 'is_featured', 'is_published', 'has_swimming_pool', 'created_at')
    search_fields = ('title', 'description', 'address', 'landmark_notes')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('features',)
    inlines = [PropertyImageInline]
    actions = ['mark_published', 'mark_unpublished', 'mark_featured', 'mark_sold', 'mark_rented']

    @admin.action(description="Publish selected properties")
    def mark_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected properties")
    def mark_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Toggle as Featured")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Mark as SOLD")
    def mark_sold(self, request, queryset):
        queryset.update(status=Property.Status.SOLD)

    @admin.action(description="Mark as RENTED")
    def mark_rented(self, request, queryset):
        queryset.update(status=Property.Status.RENTED)
