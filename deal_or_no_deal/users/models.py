from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


class User(AbstractUser):
    # Personal Information
    other_names = models.CharField(max_length=50, blank=True, null=True, verbose_name="Other Names")
    phone_number = PhoneNumberField(unique=True, blank=False, null=False, verbose_name="Phone Number")
    date_of_birth = models.DateField(blank=False, null=False, verbose_name="Date of Birth")
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='prefer_not_to_say', verbose_name="Gender")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Profile Picture")

    # Identification Details
    ID_TYPES = (
        ('national_ID', 'National ID'),
        ('driver_license', 'Driver’s License'),
        ('passport', 'Passport'),
        ('others', 'Others'),
    )
    id_type = models.CharField(max_length=25, choices=ID_TYPES, null=True, blank=True, verbose_name="ID Type")
    id_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="ID Number")
    id_image = models.ImageField(upload_to='id_cards/', blank=True, null=True, verbose_name="ID Image")

    # Address
    address = models.TextField(max_length=400, blank=True, null=True, verbose_name="Address")

    # Wallet
    cash = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Cash Balance")
    coins = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Coins Balance")

    # Rank and Limits
    RANK_CHOICES = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    )
    rank = models.CharField(max_length=10, choices=RANK_CHOICES, default='bronze', verbose_name="Rank")
    lower_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Lower Limit")
    upper_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Upper Limit")

    # Verification and Status
    verification_status = models.BooleanField(default=False, verbose_name="Verification Status")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    is_staff = models.BooleanField(default=False, verbose_name="Staff Status")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deleted At")

    # Social Media Links (Optional)
    twitter_profile = models.URLField(blank=True, null=True, verbose_name="Twitter Profile")
    facebook_profile = models.URLField(blank=True, null=True, verbose_name="Facebook Profile")
    linkedin_profile = models.URLField(blank=True, null=True, verbose_name="LinkedIn Profile")

    # Slug for Clean URLs
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the username, ensuring uniqueness
        if not self.slug:
            base_slug = slugify(self.username)
            slug = base_slug
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(5)}"
            self.slug = slug

        # Ensure verification status is updated based on ID details
        if self.id_image and self.id_number and self.id_type:
            self.verification_status = True
        else:
            self.verification_status = False

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Soft delete: set deleted_at and deactivate user
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def clean(self):
        # Validate ID fields
        if self.id_type and not self.id_number:
            raise ValidationError({'id_number': 'ID number is required when ID type is provided.'})
        if self.id_number and not self.id_type:
            raise ValidationError({'id_type': 'ID type is required when ID number is provided.'})

        # Ensure positive lower and upper limits
        if self.lower_limit and self.lower_limit < 0:
            raise ValidationError({'lower_limit': 'Lower limit must be a positive value.'})
        if self.upper_limit and self.upper_limit < 0:
            raise ValidationError({'upper_limit': 'Upper limit must be a positive value.'})
        if self.lower_limit and self.upper_limit and self.lower_limit > self.upper_limit:
            raise ValidationError('Lower limit must be less than the upper limit.')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
            models.Index(fields=['slug']),
        ]
