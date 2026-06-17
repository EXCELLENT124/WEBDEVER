from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from .models import WebsiteApplication, ApplicationMessage
from .forms import WebsiteApplicationForm, ApplicationMessageForm

from services.models import WebsiteType, AdditionalService, MobileAppType


def safe_send_mail(subject, message, recipient_list):
    """
    Send email safely.
    If email fails, the website form must still submit successfully.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=True,
        )
    except Exception:
        pass


# =========================================
# WEBSITE APPLICATION VIEW
# =========================================
def apply_view(request):
    website_types = WebsiteType.objects.filter(is_active=True)
    additional_services = AdditionalService.objects.filter(is_active=True)

    if request.method == 'POST':
        form = WebsiteApplicationForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    application = form.save()

                subject = f'Website Application Received - {application.project_title}'
                message = f"""
Hi {application.first_name},

Thank you for submitting your website application.

Project: {application.project_title}
Type: {application.website_type}

We will contact you within 24–48 hours.

Regards,
SOFTWAP Team
"""

                safe_send_mail(
                    subject,
                    message,
                    [application.email]
                )

                admin_subject = f'New Website Application: {application.project_title}'
                admin_message = f"""
New WEBSITE application received:

Name: {application.first_name} {application.last_name}
Email: {application.email}
Phone: {application.phone}

Project: {application.project_title}
Type: {application.website_type}
Budget: {application.budget_range}
"""

                safe_send_mail(
                    admin_subject,
                    admin_message,
                    [settings.DEFAULT_FROM_EMAIL]
                )

                messages.success(request, 'Website application submitted successfully!')
                return redirect('application_success', application_id=application.id)

            except Exception as e:
                messages.error(request, f'Error submitting application: {str(e)}')

    else:
        form = WebsiteApplicationForm()

    return render(request, 'applications/apply.html', {
        'title': 'Apply for a Website',
        'form': form,
        'website_types': website_types,
        'additional_services': additional_services,
        'application_type': 'website'
    })


# =========================================
# MOBILE APPLICATION VIEW
# =========================================
def apply_mobile_view(request):
    mobile_types = MobileAppType.objects.filter(is_active=True)

    if request.method == 'POST':
        form = WebsiteApplicationForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    application = form.save(commit=False)
                    application.application_type = 'mobile'
                    application.save()
                    form.save_m2m()

                subject = f'Mobile App Application Received - {application.project_title}'
                message = f"""
Hi {application.first_name},

Thank you for submitting your mobile application request.

Project: {application.project_title}
Budget: {application.budget_range}

We will contact you within 24–48 hours.

Regards,
SOFTWAP Team
"""

                safe_send_mail(
                    subject,
                    message,
                    [application.email]
                )

                admin_subject = f'New Mobile App Application: {application.project_title}'
                admin_message = f"""
New MOBILE application received:

Name: {application.first_name} {application.last_name}
Email: {application.email}
Phone: {application.phone}

Project: {application.project_title}
Budget: {application.budget_range}
"""

                safe_send_mail(
                    admin_subject,
                    admin_message,
                    [settings.DEFAULT_FROM_EMAIL]
                )

                messages.success(request, 'Mobile application submitted successfully!')
                return redirect('application_success', application_id=application.id)

            except Exception as e:
                messages.error(request, f'Error submitting application: {str(e)}')

    else:
        form = WebsiteApplicationForm()

    return render(request, 'applications/apply_mobile.html', {
        'title': 'Apply for Mobile Application',
        'form': form,
        'mobile_types': mobile_types,
        'application_type': 'mobile'
    })


# =========================================
# SUCCESS VIEW
# =========================================
def application_success_view(request, application_id):
    application = get_object_or_404(WebsiteApplication, id=application_id)

    return render(request, 'applications/success.html', {
        'title': 'Application Submitted',
        'application': application,
    })


# =========================================
# STATUS VIEW
# =========================================
def application_status_view(request, application_id):
    application = get_object_or_404(WebsiteApplication, id=application_id)

    if request.method == 'POST':
        message_form = ApplicationMessageForm(request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.application = application
            message.save()

            messages.success(request, 'Message sent successfully.')
            return redirect('application_status', application_id=application.id)

    else:
        message_form = ApplicationMessageForm()

    return render(request, 'applications/status.html', {
        'title': f'Status - {application.project_title}',
        'application': application,
        'messages': application.messages.all(),
        'message_form': message_form,
    })


# =========================================
# AJAX DATA
# =========================================
def services_ajax_data(request):
    website_types_data = [
        {
            'id': wt.id,
            'name': wt.get_name_display(),
            'min_price': float(wt.min_price),
            'max_price': float(wt.max_price),
            'price_range': wt.get_price_range(),
            'days': wt.estimated_days,
        }
        for wt in WebsiteType.objects.filter(is_active=True)
    ]

    mobile_types_data = [
        {
            'id': mt.id,
            'name': mt.name,
            'min_price': float(mt.min_price),
            'max_price': float(mt.max_price),
            'days': mt.estimated_days,
        }
        for mt in MobileAppType.objects.filter(is_active=True)
    ]

    services_data = [
        {
            'id': s.id,
            'name': s.get_name_display(),
            'price': float(s.price),
            'billing': s.get_billing_cycle_display(),
        }
        for s in AdditionalService.objects.filter(is_active=True)
    ]

    return {
        'website_types': website_types_data,
        'mobile_types': mobile_types_data,
        'additional_services': services_data,
    }