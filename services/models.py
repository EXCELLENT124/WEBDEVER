from django.db import models
from django.utils.text import slugify


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
    ]

    name = models.CharField(max_length=50, choices=WEBSITE_CATEGORIES, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    features = models.TextField(help_text="List key features, one per line")
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField(help_text="Estimated days to complete")
    icon = models.CharField(max_length=50, default='globe')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Website Type'
        verbose_name_plural = 'Website Types'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    def get_price_range(self):
        return f"R{self.min_price:,.0f} - R{self.max_price:,.0f}"

    def get_feature_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


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
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES, default='once')
    features = models.TextField(help_text="List features included, one per line", blank=True)
    is_required = models.BooleanField(default=False, help_text="Required for all websites")
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Additional Service'
        verbose_name_plural = 'Additional Services'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_name_display()} - R{self.price:,.0f}/{self.get_billing_cycle_display().lower()}"

    def get_price_display(self):
        cycle = self.get_billing_cycle_display().lower()
        return f"R{self.price:,.0f}/{cycle.replace('one-time', 'once')}"

    def get_feature_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class ServicePackage(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    website_type = models.ForeignKey(WebsiteType, on_delete=models.CASCADE, related_name='packages')
    additional_services = models.ManyToManyField(AdditionalService, blank=True, related_name='packages')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Package discount percentage")
    is_popular = models.BooleanField(default=False, help_text="Mark as popular/recommended")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Service Package'
        verbose_name_plural = 'Service Packages'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def calculate_total_price(self):
        base_price = self.website_type.min_price
        additional_total = sum(service.price for service in self.additional_services.filter(is_active=True))
        subtotal = base_price + additional_total
        discount = subtotal * (self.discount_percentage / 100)
        return subtotal - discount

    def get_total_price_display(self):
        return f"R{self.calculate_total():,.0f}"

    def calculate_total(self):
        return self.calculate_total_price()
