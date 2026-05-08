from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import WebsiteType, AdditionalService, ServicePackage


def website_type_list_view(request):
    """List all available website types."""
    website_types = WebsiteType.objects.filter(is_active=True)
    
    context = {
        'title': 'Website Types',
        'website_types': website_types,
    }
    return render(request, 'services/website_type_list.html', context)


def website_type_detail_view(request, slug):
    """Detail view for a specific website type."""
    website_type = get_object_or_404(WebsiteType, slug=slug, is_active=True)
    related_packages = ServicePackage.objects.filter(website_type=website_type, is_active=True)[:3]
    
    context = {
        'title': website_type.get_name_display(),
        'website_type': website_type,
        'related_packages': related_packages,
    }
    return render(request, 'services/website_type_detail.html', context)


def additional_service_list_view(request):
    """List all additional services."""
    services = AdditionalService.objects.filter(is_active=True)
    
    context = {
        'title': 'Additional Services',
        'services': services,
    }
    return render(request, 'services/additional_service_list.html', context)


def package_list_view(request):
    """List all service packages."""
    packages = ServicePackage.objects.filter(is_active=True)
    
    context = {
        'title': 'Service Packages',
        'packages': packages,
    }
    return render(request, 'services/package_list.html', context)


def package_detail_view(request, slug):
    """Detail view for a service package."""
    package = get_object_or_404(ServicePackage, slug=slug, is_active=True)
    
    context = {
        'title': package.name,
        'package': package,
    }
    return render(request, 'services/package_detail.html', context)


def get_website_type_price(request, website_type_id):
    """AJAX endpoint to get price range for a website type."""
    try:
        website_type = WebsiteType.objects.get(id=website_type_id, is_active=True)
        return JsonResponse({
            'success': True,
            'min_price': float(website_type.min_price),
            'max_price': float(website_type.max_price),
            'price_range': website_type.get_price_range(),
            'estimated_days': website_type.estimated_days,
        })
    except WebsiteType.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Website type not found'
        }, status=404)


def get_additional_service_price(request, service_id):
    """AJAX endpoint to get price for an additional service."""
    try:
        service = AdditionalService.objects.get(id=service_id, is_active=True)
        return JsonResponse({
            'success': True,
            'price': float(service.price),
            'billing_cycle': service.get_billing_cycle_display(),
            'price_display': service.get_price_display(),
        })
    except AdditionalService.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Service not found'
        }, status=404)
