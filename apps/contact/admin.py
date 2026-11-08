from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'is_read', 'is_archived', 'created_at')
    list_filter = ('is_read', 'is_archived', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    actions = ['mark_read', 'mark_unread', 'mark_archived']

    @admin.action(description="Mark selected messages as READ")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as UNREAD")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)

    @admin.action(description="Archive selected messages")
    def mark_archived(self, request, queryset):
        queryset.update(is_archived=True)
