from django.contrib import admin
from .models import WebsiteApplication, ApplicationMessage


# =========================================
# APPLICATION MESSAGE INLINE
# =========================================
class ApplicationMessageInline(admin.TabularInline):
    model = ApplicationMessage
    extra = 1
    fields = (
        'sender_name',
        'sender_email',
        'is_from_staff',
        'message',
        'created_at',
    )
    readonly_fields = ('created_at',)


# =========================================
# WEBSITE APPLICATION ADMIN
# =========================================
@admin.register(WebsiteApplication)
class WebsiteApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'project_title',
        'get_full_name',
        'application_type',
        'website_type',
        'budget_range',
        'status',
        'priority',
        'created_at',
    )

    list_filter = (
        'application_type',
        'status',
        'priority',
        'website_type',
        'budget_range',
        'created_at',
    )

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'project_title',
        'project_description',
    )

    list_editable = (
        'status',
        'priority',
    )

    date_hierarchy = 'created_at'

    inlines = (ApplicationMessageInline,)

    fieldsets = (
        ('Application Type', {
            'fields': ('application_type',)
        }),

        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'company_name',
            )
        }),

        ('Project Details', {
            'fields': (
                'website_type',
                'mobile_app_type',
                'project_title',
                'project_description',
            )
        }),

        ('Budget & Timeline', {
            'fields': (
                'budget_range',
                'preferred_timeline',
                'quoted_price',
            )
        }),

        ('Additional Services', {
            'fields': ('additional_services',)
        }),

        ('Design & Content', {
            'fields': (
                'design_preferences',
                'has_logo',
                'has_content',
                'has_domain',
            )
        }),

        ('Features', {
            'fields': ('features_needed',)
        }),

        ('Status & Notes', {
            'fields': (
                'status',
                'priority',
                'admin_notes',
            )
        }),
    )

    filter_horizontal = ('additional_services',)

    actions = (
        'mark_as_under_review',
        'mark_as_quoted',
        'mark_as_accepted',
        'mark_as_in_progress',
    )

    def mark_as_under_review(self, request, queryset):
        queryset.update(status='under_review')
    mark_as_under_review.short_description = "Mark selected as Under Review"

    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
    mark_as_quoted.short_description = "Mark selected as Quote Sent"

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
    mark_as_quoted.short_description = "Mark selected as Quote Accepted"

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark selected as In Progress"


# =========================================
# APPLICATION MESSAGE ADMIN
# =========================================
@admin.register(ApplicationMessage)
class ApplicationMessageAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'sender_name',
        'is_from_staff',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_from_staff',
        'is_read',
        'created_at',
    )

    search_fields = (
        'sender_name',
        'sender_email',
        'message',
    )

    list_editable = ('is_read',)

    date_hierarchy = 'created_at'