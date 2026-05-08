from django.contrib import admin
from .models import WebsiteType, AdditionalService, ServicePackage


@admin.register(WebsiteType)
class WebsiteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_price_range', 'estimated_days', 'is_active', 'display_order']
    list_filter = ['is_active', 'name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Pricing & Timeline', {
            'fields': ('min_price', 'max_price', 'estimated_days')
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter features one per line'
        }),
        ('Status', {
            'fields': ('is_active', 'display_order')
        }),
    )


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'billing_cycle', 'is_required', 'is_recommended', 'is_active']
    list_filter = ['billing_cycle', 'is_required', 'is_recommended', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_required', 'is_recommended']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'billing_cycle')
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter features one per line'
        }),
        ('Settings', {
            'fields': ('is_required', 'is_recommended', 'is_active', 'display_order')
        }),
    )


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_type', 'discount_percentage', 'is_popular', 'is_active', 'display_order']
    list_filter = ['website_type', 'is_popular', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['additional_services']
    list_editable = ['is_active', 'is_popular']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'website_type')
        }),
        ('Services', {
            'fields': ('additional_services',)
        }),
        ('Pricing', {
            'fields': ('discount_percentage',)
        }),
        ('Settings', {
            'fields': ('is_popular', 'is_active', 'display_order')
        }),
    )
