from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=200, default="General Inquiry")
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    is_archived = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} ({self.subject}) - {self.created_at.strftime('%Y-%m-%d')}"
