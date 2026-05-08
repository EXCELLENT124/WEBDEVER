from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import WebsiteApplication, ApplicationMessage
from .forms import WebsiteApplicationForm, ApplicationMessageForm
from services.models import WebsiteType, AdditionalService


def apply_view(request):
    """Website application form view."""
    website_types = WebsiteType.objects.filter(is_active=True)
    additional_services = AdditionalService.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = WebsiteApplicationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    application = form.save()
                    
                    # Send confirmation email to customer
                    subject = f'Website Application Received - {application.project_title}'
                    message = f"""
Dear {application.first_name},

Thank you for submitting your website application to SOFTWAP!

We have received your request for:
Project: {application.project_title}
Website Type: {application.website_type.get_name_display()}
Estimated Budget: {application.get_estimated_total_display()}

Our team will review your application and contact you within 24-48 hours with a detailed quote.

If you have any questions, please reply to this email or contact us directly.

Best regards,
The SOFTWAP Team
"""
                    
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[application.email],
                        fail_silently=True,
                    )
                    
                    # Send notification to admin
                    admin_subject = f'New Website Application: {application.project_title}'
                    admin_message = f"""
New website application received:

Client: {application.get_full_name()}
Email: {application.email}
Phone: {application.phone}
Project: {application.project_title}
Type: {application.website_type.get_name_display()}
Estimated Price: {application.get_estimated_total_display()}

View in admin: {request.build_absolute_uri('/admin/applications/websiteapplication/')}
"""
                    
                    send_mail(
                        subject=admin_subject,
                        message=admin_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DEFAULT_FROM_EMAIL],
                        fail_silently=True,
                    )
                    
                    messages.success(request, 'Your application has been submitted successfully! We will contact you within 24-48 hours.')
                    return redirect('application_success', application_id=application.id)
            except Exception as e:
                messages.error(request, f'Error submitting application: {str(e)}. Please try again.')
    else:
        form = WebsiteApplicationForm()
    
    context = {
        'title': 'Apply for a Website',
        'form': form,
        'website_types': website_types,
        'additional_services': additional_services,
    }
    return render(request, 'applications/apply.html', context)


def application_success_view(request, application_id):
    """Success page after application submission."""
    application = get_object_or_404(WebsiteApplication, id=application_id)
    
    context = {
        'title': 'Application Submitted',
        'application': application,
    }
    return render(request, 'applications/success.html', context)


def application_status_view(request, application_id):
    """View application status and details."""
    application = get_object_or_404(WebsiteApplication, id=application_id)
    
    if request.method == 'POST':
        message_form = ApplicationMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.application = application
            message.save()
            messages.success(request, 'Your message has been sent.')
            return redirect('application_status', application_id=application.id)
    else:
        message_form = ApplicationMessageForm()
    
    messages_list = application.messages.all()
    
    context = {
        'title': f'Application Status - {application.project_title}',
        'application': application,
        'messages': messages_list,
        'message_form': message_form,
    }
    return render(request, 'applications/status.html', context)


def services_ajax_data(request):
    """AJAX endpoint to get all services data for dynamic pricing."""
    import json
    
    website_types_data = []
    for wt in WebsiteType.objects.filter(is_active=True):
        website_types_data.append({
            'id': wt.id,
            'name': wt.get_name_display(),
            'slug': wt.slug,
            'min_price': float(wt.min_price),
            'max_price': float(wt.max_price),
            'price_range': wt.get_price_range(),
            'estimated_days': wt.estimated_days,
        })
    
    services_data = []
    for service in AdditionalService.objects.filter(is_active=True):
        services_data.append({
            'id': service.id,
            'name': service.get_name_display(),
            'price': float(service.price),
            'billing_cycle': service.get_billing_cycle_display(),
            'price_display': service.get_price_display(),
        })
    
    return {
        'website_types': website_types_data,
        'additional_services': services_data,
    }
