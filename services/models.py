from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# =========================================
# WEBSITE TYPES
# =========================================

class WebsiteType(models.Model):
    WEBSITE_CATEGORIES = [
        ('one_page', 'One Page Website'),
        ('business', 'Business/Brochure Website'),
        ('ecommerce', 'E-commerce Website'),
        ('portfolio', 'Portfolio Website'),
        ('blog', 'Blog/Content Website'),
        ('custom_app', 'Custom Web Application'),
        ('landing_page', 'Landing Page'),
        ('membership', 'Membership/Subscription Site'),
        ('real_estate', 'Real Estate Website'),
        ('restaurant', 'Restaurant/Food Website'),
        ('booking', 'Booking/Appointment Website'),
        ('educational', 'Educational/Learning Platform'),
        ('nonprofit', 'Non-Profit/Charity Website'),
        ('corporate', 'Corporate Enterprise Website'),
        ('marketplace', 'Online Marketplace'),
        ('starter_mobile_app', 'Starter Mobile App'),
        ('business_mobile_app', 'Business Mobile App'),
        ('ecommerce_mobile_app', 'E-commerce Mobile App'),
        ('custom_mobile_app', 'Custom Mobile App'),
    ]

    name = models.CharField(max_length=50, choices=WEBSITE_CATEGORIES, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    features = models.TextField(help_text="List key features, one per line")
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    icon = models.CharField(max_length=50, default='globe')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Website Type"
        verbose_name_plural = "Website Types"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    def get_price_range(self):
        return f"R{self.min_price:,.0f} - R{self.max_price:,.0f}"

    def get_feature_list(self):
        return [
            f.strip()
            for f in self.features.split('\n')
            if f.strip()
        ]


# =========================================
# MOBILE APPLICATION TYPES
# =========================================

class MobileAppType(models.Model):
    APP_CATEGORIES = [
        ('basic_app', 'Basic Mobile App (Info App)'),
        ('business_app', 'Business Mobile App'),
        ('ecommerce_app', 'E-commerce Mobile App'),
        ('booking_app', 'Booking/Appointment App'),
        ('social_app', 'Social Networking App'),
        ('marketplace_app', 'Marketplace App'),
        ('custom_app', 'Custom Mobile Application'),
        ('education_app', 'Education/Learning App'),
        ('delivery_app', 'Delivery/Logistics App'),
        ('finance_app', 'Finance/Fintech App'),
        ('on_demand_app', 'On-Demand Service App'),
    ]

    name = models.CharField(max_length=50, choices=APP_CATEGORIES, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    description = models.TextField()
    features = models.TextField(help_text="List key features, one per line")

    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=15000
    )

    max_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=250000
    )

    estimated_days = models.PositiveIntegerField(
        help_text="Estimated days to complete"
    )

    icon = models.CharField(max_length=50, default='mobile-alt')

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Mobile App Type"
        verbose_name_plural = "Mobile App Types"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    def get_price_range(self):
        return f"R{self.min_price:,.0f} - R{self.max_price:,.0f}"

    def get_feature_list(self):
        return [
            f.strip()
            for f in self.features.split('\n')
            if f.strip()
        ]


# =========================================
# ADDITIONAL SERVICES
# =========================================

class AdditionalService(models.Model):
    SERVICE_TYPES = [
        ('hosting', 'Web Hosting'),
        ('domain', 'Domain Registration'),
        ('ssl', 'SSL Certificate'),
        ('maintenance', 'Website Maintenance'),
        ('seo', 'SEO Optimization'),
        ('content', 'Content Writing'),
        ('logo', 'Logo Design'),
        ('social', 'Social Media Integration'),
        ('analytics', 'Analytics Setup'),
        ('backup', 'Backup Service'),
        ('security', 'Security Monitoring'),
        ('support', 'Technical Support'),
        ('training', 'Website Training'),
        ('migration', 'Website Migration'),
        ('speed', 'Speed Optimization'),
    ]

    BILLING_CYCLES = [
        ('once', 'One-time'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=50, choices=SERVICE_TYPES, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    billing_cycle = models.CharField(
        max_length=20,
        choices=BILLING_CYCLES,
        default='once'
    )

    features = models.TextField(blank=True)

    icon = models.CharField(max_length=50, default='cog')

    is_required = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Additional Service"
        verbose_name_plural = "Additional Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_name_display()} - R{self.price:,.0f}"

    def get_price_display(self):
        cycle = self.get_billing_cycle_display().lower()

        if cycle == 'one-time':
            return f"R{self.price:,.0f} once"

        return f"R{self.price:,.0f}/{cycle}"

    def get_feature_list(self):
        return [
            f.strip()
            for f in self.features.split('\n')
            if f.strip()
        ]


# =========================================
# SERVICE PACKAGES
# =========================================

class ServicePackage(models.Model):
    name = models.CharField(max_length=100)

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    description = models.TextField()

    website_type = models.ForeignKey(
        WebsiteType,
        on_delete=models.CASCADE,
        related_name='packages',
        null=True,
        blank=True
    )

    mobile_app_type = models.ForeignKey(
        MobileAppType,
        on_delete=models.CASCADE,
        related_name='packages',
        null=True,
        blank=True
    )

    additional_services = models.ManyToManyField(
        AdditionalService,
        blank=True
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Service Package"
        verbose_name_plural = "Service Packages"

    def clean(self):
        if self.website_type and self.mobile_app_type:
            raise ValidationError(
                "A package can only belong to a Website Type OR a Mobile App Type."
            )

        if not self.website_type and not self.mobile_app_type:
            raise ValidationError(
                "A package must belong to either a Website Type or Mobile App Type."
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def calculate_total_price(self):
        base_price = 0

        if self.website_type:
            base_price = self.website_type.min_price
        elif self.mobile_app_type:
            base_price = self.mobile_app_type.min_price

        additional_total = sum(
            service.price
            for service in self.additional_services.filter(is_active=True)
        )

        subtotal = base_price + additional_total

        discount = subtotal * (
            self.discount_percentage / 100
        )

        return subtotal - discount

    def get_total_price_display(self):
        return f"R{self.calculate_total_price():,.0f}"
