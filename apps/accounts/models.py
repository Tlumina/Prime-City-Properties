from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        STAFF = 'STAFF', 'Staff Member'
        AGENT = 'AGENT', 'Real Estate Agent'
        CUSTOMER = 'CUSTOMER', 'Customer / Buyer'

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, help_text="User primary email address")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. +234 806 854 2996")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        ordering = ['-date_joined']

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.email

    def save(self, *args, **kwargs):
        if not self.username or self.username == '':
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def is_real_estate_agent(self):
        return self.role in [self.Role.ADMIN, self.Role.STAFF, self.Role.AGENT]
