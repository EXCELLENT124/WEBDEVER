from .models import WebsiteType, AdditionalService, ServicePackage


def services_processor(request):
    """Context processor to make services available in all templates."""
    return {
        'all_website_types': WebsiteType.objects.filter(is_active=True),
        'all_additional_services': AdditionalService.objects.filter(is_active=True),
        'all_packages': ServicePackage.objects.filter(is_active=True),
    }