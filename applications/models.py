from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from services.models import WebsiteType, AdditionalService


# ==============================
# WEBSITE APPLICATION
# ==============================
class WebsiteApplication(models.Model):

    APPLICATION_TYPE = [
        ('website', 'Website'),
        ('mobile', 'Mobile Application'),
    ]

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

    # TYPE SWITCH (IMPORTANT)
    application_type = models.CharField(
        max_length=20,
        choices=APPLICATION_TYPE,
        default='website'
    )

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^(\+27|0)[6-8][0-9]{8}$')]
    )
    company_name = models.CharField(max_length=200, blank=True)

    # WEBSITE TYPE (optional now)
    website_type = models.ForeignKey(
        WebsiteType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='applications'
    )

    # MOBILE TYPE (NEW)
    mobile_app_type = models.ForeignKey(
        'MobileAppType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )

    project_title = models.CharField(max_length=200)
    project_description = models.TextField()

    budget_range = models.CharField(max_length=20, choices=BUDGET_RANGES, default='custom')
    preferred_timeline = models.PositiveIntegerField(blank=True, null=True)

    additional_services = models.ManyToManyField(
        AdditionalService,
        blank=True,
        related_name='applications'
    )

    design_preferences = models.TextField(blank=True)
    has_logo = models.BooleanField(default=False)
    has_content = models.BooleanField(default=False)
    has_domain = models.BooleanField(default=False)

    features_needed = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')

    admin_notes = models.TextField(blank=True)
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_title} - {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_estimated_total(self):
        if self.application_type == "website":
            base = self.website_type.min_price if self.website_type else 0
        else:
            base = self.mobile_app_type.min_price if self.mobile_app_type else 0

        additional = sum(
            s.price for s in self.additional_services.filter(is_active=True)
        )

        return base + additional

    def get_estimated_total_display(self):
        return f"R{self.get_estimated_total():,.0f}"


# ==============================
# MOBILE APP TYPE (KEEP THIS)
# ==============================
class MobileAppType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    icon = models.CharField(max_length=50, default='mobile')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_price_range(self):
        return f"R{self.min_price:,.0f} - {self.max_price:,.0f}"


# ==============================
# MESSAGES
# ==============================
class ApplicationMessage(models.Model):
    application = models.ForeignKey(
        WebsiteApplication,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    message = models.TextField()
    is_from_staff = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender_name}"