from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from services.models import WebsiteType, AdditionalService


class WebsiteApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('quoted', 'Quote Sent'),
        ('accepted', 'Quote Accepted'),
        ('in_progress', 'In Development'),
        ('testing', 'Testing Phase'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('normal', 'Normal Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]

    BUDGET_RANGES = [
        ('under_5k', 'Under R5,000'),
        ('5k_to_10k', 'R5,000 - R10,000'),
        ('10k_to_20k', 'R10,000 - R20,000'),
        ('20k_to_50k', 'R20,000 - R50,000'),
        ('50k_plus', 'R50,000+'),
        ('custom', 'Custom Budget'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^(\+27|0)[6-8][0-9]{8}$',
            message='Enter a valid South African phone number'
        )
    ])
    company_name = models.CharField(max_length=200, blank=True, help_text="Optional - for business websites")
    
    # Project Details
    website_type = models.ForeignKey(WebsiteType, on_delete=models.CASCADE, related_name='applications')
    project_title = models.CharField(max_length=200)
    project_description = models.TextField(help_text="Describe what you need for your website")
    
    # Budget and Timeline
    budget_range = models.CharField(max_length=20, choices=BUDGET_RANGES, default='custom')
    preferred_timeline = models.PositiveIntegerField(help_text="Preferred completion time in days", blank=True, null=True)
    
    # Additional Services
    additional_services = models.ManyToManyField(AdditionalService, blank=True, related_name='applications')
    
    # Design Preferences
    design_preferences = models.TextField(blank=True, help_text="Color schemes, style preferences, examples of websites you like")
    has_logo = models.BooleanField(default=False, help_text="Do you have a logo?")
    has_content = models.BooleanField(default=False, help_text="Do you have content ready (text, images)?")
    has_domain = models.BooleanField(default=False, help_text="Do you have a domain name registered?")
    
    # Additional Features
    features_needed = models.TextField(blank=True, help_text="Specific features needed (e.g., contact form, gallery, booking system)")
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Admin fields
    admin_notes = models.TextField(blank=True, help_text="Internal notes for staff")
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Website Application'
        verbose_name_plural = 'Website Applications'
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['email', 'status']),
        ]

    def __str__(self):
        return f"{self.project_title} - {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_services_summary(self):
        services = list(self.additional_services.filter(is_active=True))
        if not services:
            return "No additional services"
        return ", ".join([s.get_name_display() for s in services])

    def get_estimated_total(self):
        base = self.website_type.min_price
        additional = sum(s.price for s in self.additional_services.filter(is_active=True))
        return base + additional

    def get_estimated_total_display(self):
        return f"R{self.get_estimated_total():,.0f}"


class ApplicationMessage(models.Model):
    application = models.ForeignKey(WebsiteApplication, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    message = models.TextField()
    is_from_staff = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Application Message'
        verbose_name_plural = 'Application Messages'

    def __str__(self):
        return f"Message from {self.sender_name} on {self.created_at.strftime('%Y-%m-%d')}"
