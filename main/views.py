from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string          # <-- add this import
from applications.forms import ContactForm
from services.models import WebsiteType, AdditionalService, ServicePackage
# Import your Order model (adjust the import path to your actual app)
from orders.models import Order   # e.g. if your app is named 'orders'


def home_view(request):
    """Home page view with featured services and packages."""
    featured_website_types = WebsiteType.objects.filter(is_active=True)[:6]
    popular_packages = ServicePackage.objects.filter(is_active=True, is_popular=True)[:3]
    featured_services = AdditionalService.objects.filter(is_active=True, is_recommended=True)[:6]
    
    context = {
        'featured_website_types': featured_website_types,
        'popular_packages': popular_packages,
        'featured_services': featured_services,
    }
    return render(request, 'main/home.html', context)


def about_view(request):
    """About page view."""
    context = {
        'title': 'About Us',
        'company_name': 'SOFTWAP',
    }
    return render(request, 'main/about.html', context)


def contact_view(request):
    """Contact page view with form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            phone = form.cleaned_data.get('phone', '')
            
            full_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}
"""
            
            try:
                send_mail(
                    subject=f'Contact Form: {subject}',
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'Error sending message: {str(e)}')
    else:
        form = ContactForm()
    
    context = {
        'title': 'Contact Us',
        'form': form,
    }
    return render(request, 'main/contact.html', context)


def services_overview_view(request):
    """Services overview page."""
    website_types = WebsiteType.objects.filter(is_active=True)
    additional_services = AdditionalService.objects.filter(is_active=True)
    
    context = {
        'title': 'Our Services',
        'website_types': website_types,
        'additional_services': additional_services,
    }
    return render(request, 'main/services_overview.html', context)


def pricing_view(request):
    """Pricing page with detailed pricing information."""
    website_types = WebsiteType.objects.filter(is_active=True)
    additional_services = AdditionalService.objects.filter(is_active=True)
    packages = ServicePackage.objects.filter(is_active=True)
    
    context = {
        'title': 'Pricing',
        'website_types': website_types,
        'additional_services': additional_services,
        'packages': packages,
    }
    return render(request, 'main/pricing.html', context)


# ========== NEW: Order Confirmation View with Email ==========
def place_order_view(request):
    """Create an order and send confirmation email."""
    if request.method == 'POST':
        # --- Replace this block with your actual order creation logic ---
        # Example: creating an order from form data (adjust field names)
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        service = ServicePackage.objects.get(id=request.POST.get('service_id'))
        amount = request.POST.get('amount')
        
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            service=service,
            amount=amount,
            # Add other fields as needed
        )
        # ----------------------------------------------------------------

        # Send order confirmation email
        subject = f'Order #{order.id} - Confirmed'
        html_message = render_to_string('emails/order_confirmed.html', {'order': order})
        plain_message = f'Your order #{order.id} has been received and is being processed.'

        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer_email],        # ensure Order model has customer_email field
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, 'Order placed successfully! A confirmation email has been sent.')
        except Exception as e:
            messages.error(request, f'Order saved but email could not be sent: {str(e)}')

        return redirect('home')  # change to your success URL

    # If not POST, render order form (optional)
    return render(request, 'orders/place_order.html')  # create this template or adjust
