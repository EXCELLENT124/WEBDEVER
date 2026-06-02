from django.contrib import admin
from .models import (
    WebsiteType,
    MobileAppType,
    AdditionalService,
    ServicePackage,
)


@admin.register(WebsiteType)
class WebsiteTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_price_range',
        'estimated_days',
        'is_active',
        'display_order'
    ]

    list_filter = [
        'is_active',
        'name'
    ]

    search_fields = [
        'name',
        'description'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = [
        'is_active',
        'display_order'
    ]

    ordering = [
        'display_order',
        'name'
    ]


@admin.register(MobileAppType)
class MobileAppTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_price_range',
        'estimated_days',
        'is_active',
        'display_order'
    ]

    list_filter = [
        'is_active',
        'name'
    ]

    search_fields = [
        'name',
        'description'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = [
        'is_active',
        'display_order'
    ]

    ordering = [
        'display_order',
        'name'
    ]


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'billing_cycle',
        'is_required',
        'is_recommended',
        'is_active'
    ]

    list_filter = [
        'billing_cycle',
        'is_required',
        'is_recommended',
        'is_active'
    ]

    search_fields = [
        'name',
        'description'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = [
        'is_active',
        'is_required',
        'is_recommended'
    ]


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'website_type',
        'mobile_app_type',
        'discount_percentage',
        'is_popular',
        'is_active'
    ]

    list_filter = [
        'is_popular',
        'is_active'
    ]

    search_fields = [
        'name',
        'description'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    filter_horizontal = [
        'additional_services'
    ]

    list_editable = [
        'is_active',
        'is_popular'
    ]