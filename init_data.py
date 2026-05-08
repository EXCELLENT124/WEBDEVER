#!/usr/bin/env python
"""
Initialize database with website types and services data.
Run with: python init_data.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webdever_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from services.models import WebsiteType, AdditionalService


def create_website_types():
    """Create initial website types with pricing."""
    website_types = [
        {
            'name': 'one_page',
            'description': 'A single-page website that presents all your content in a scrolling format. Perfect for simple business presence, personal portfolios, or event promotions. Simple, elegant, and effective.',
            'features': 'Single scrolling page design\nMobile responsive layout\nContact form integration\nSocial media links\nBasic SEO setup\nFast loading speed',
            'min_price': 2500,
            'max_price': 4500,
            'estimated_days': 5,
            'icon': 'file-alt',
            'display_order': 1,
        },
        {
            'name': 'business',
            'description': 'A professional multi-page website for established businesses. Includes multiple sections, service pages, and all essential business features to showcase your company online.',
            'features': 'Up to 10 custom pages\nSEO optimization\nContact forms with validation\nGoogle Maps integration\nBlog/News section\nSocial media integration\nImage galleries',
            'min_price': 4000,
            'max_price': 8000,
            'estimated_days': 21,
            'icon': 'building',
            'display_order': 2,
        },
        {
            'name': 'ecommerce',
            'description': 'A complete online store with secure payment processing, inventory management, and customer accounts. Everything you need to start selling online and grow your business.',
            'features': 'Unlimited product listings\nSecure payment gateway\nInventory management\nCustomer accounts\nOrder tracking system\nShopping cart & checkout\nProduct categories & filters',
            'min_price': 10000,
            'max_price': 25000,
            'estimated_days': 42,
            'icon': 'shopping-cart',
            'display_order': 3,
        },
        {
            'name': 'portfolio',
            'description': 'Showcase your work with stunning visual galleries and project presentations. Perfect for creatives, photographers, designers, and artists who want to display their portfolio beautifully.',
            'features': 'Image galleries with lightbox\nProject case studies\nBefore/after sliders\nClient testimonials\nSkills/services showcase\nContact form\nSocial integration',
            'min_price': 3500,
            'max_price': 6000,
            'estimated_days': 18,
            'icon': 'paint-brush',
            'display_order': 4,
        },
        {
            'name': 'blog',
            'description': 'A content-focused platform with powerful publishing tools. Perfect for bloggers, content creators, news sites, and anyone who wants to share content regularly with their audience.',
            'features': 'Article management system\nCategories & tags\nSocial sharing buttons\nComments system\nNewsletter signup\nAuthor profiles\nRelated posts',
            'min_price': 4500,
            'max_price': 8500,
            'estimated_days': 21,
            'icon': 'blog',
            'display_order': 5,
        },
        {
            'name': 'custom_app',
            'description': 'Bespoke web solutions tailored to your specific requirements. Database-driven applications with custom functionality built exactly to your business needs.',
            'features': 'Custom functionality\nDatabase integration\nUser management system\nAPI integrations\nAdmin dashboard\nReporting & analytics\nAutomated workflows',
            'min_price': 15000,
            'max_price': 50000,
            'estimated_days': 60,
            'icon': 'rocket',
            'display_order': 6,
        },
        {
            'name': 'landing_page',
            'description': 'High-converting single-page website designed for marketing campaigns. Focused on driving specific actions like sign-ups, sales, or lead generation.',
            'features': 'Single page design\nCall-to-action optimization\nA/B testing ready\nFast loading\nMobile optimized\nAnalytics integration\nForm capture',
            'min_price': 2000,
            'max_price': 4000,
            'estimated_days': 7,
            'icon': 'bullhorn',
            'display_order': 7,
        },
        {
            'name': 'membership',
            'description': 'Subscription-based content platform with protected content areas. Perfect for online courses, membership sites, and premium content businesses.',
            'features': 'User registration\nContent protection\nPayment integration\nMember dashboard\nSubscription management\nDrip content\nCommunity features',
            'min_price': 8000,
            'max_price': 20000,
            'estimated_days': 35,
            'icon': 'users',
            'display_order': 8,
        },
        {
            'name': 'real_estate',
            'description': 'Property listing website with search, filters, and agent profiles. Perfect for real estate agencies, property developers, and rental management companies.',
            'features': 'Property listings\nSearch & filter\nAgent profiles\nBooking viewings\nMap integration\nPhoto galleries\nMortgage calculator',
            'min_price': 8000,
            'max_price': 18000,
            'estimated_days': 28,
            'icon': 'home',
            'display_order': 9,
        },
        {
            'name': 'restaurant',
            'description': 'Restaurant and food business website with menu display, table booking, and online ordering capabilities. Perfect for restaurants, cafes, and food delivery businesses.',
            'features': 'Online menu\nTable booking\nOrder online\nPhoto gallery\nReviews system\nLocation map\nOpening hours',
            'min_price': 5000,
            'max_price': 12000,
            'estimated_days': 21,
            'icon': 'utensils',
            'display_order': 10,
        },
    ]
    
    for data in website_types:
        obj, created = WebsiteType.objects.update_or_create(
            name=data['name'],
            defaults=data
        )
        action = 'Created' if created else 'Updated'
        print(f"{action}: {obj.get_name_display()} - R{obj.min_price} - R{obj.max_price}")


def create_additional_services():
    """Create initial additional services with pricing."""
    services = [
        {
            'name': 'hosting',
            'description': 'Reliable web hosting with 99.9% uptime guarantee. SSD storage for fast loading speeds.',
            'price': 99,
            'billing_cycle': 'monthly',
            'features': '10GB SSD storage\nUnlimited bandwidth\nFree SSL certificate\nDaily backups\n99.9% uptime\n24/7 monitoring',
            'is_recommended': True,
            'display_order': 1,
        },
        {
            'name': 'domain',
            'description': 'Domain name registration with DNS management and privacy protection.',
            'price': 150,
            'billing_cycle': 'yearly',
            'features': '.co.za domain\nDNS management\nDomain privacy\nEmail forwarding\nAuto-renewal',
            'is_recommended': True,
            'display_order': 2,
        },
        {
            'name': 'ssl',
            'description': 'SSL certificate for HTTPS encryption and improved search rankings.',
            'price': 299,
            'billing_cycle': 'yearly',
            'features': '256-bit encryption\nSecurity seal\nSEO boost\nBrowser trust indicator\nFree installation',
            'is_recommended': True,
            'display_order': 3,
        },
        {
            'name': 'maintenance',
            'description': 'Regular website maintenance with updates, security monitoring, and support.',
            'price': 599,
            'billing_cycle': 'monthly',
            'features': 'Weekly updates\nSecurity monitoring\nPerformance optimization\nContent updates (5 pages)\nTechnical support\nMonthly reports',
            'is_recommended': True,
            'display_order': 4,
        },
        {
            'name': 'seo',
            'description': 'SEO optimization to improve search engine rankings and organic traffic.',
            'price': 1500,
            'billing_cycle': 'monthly',
            'features': 'Keyword research\nOn-page optimization\nMonthly reports\nRank tracking\nContent optimization\nLink building',
            'is_recommended': False,
            'display_order': 5,
        },
        {
            'name': 'content',
            'description': 'Professional content writing for your website pages and blog posts.',
            'price': 500,
            'billing_cycle': 'once',
            'features': 'SEO optimized copy\nProfessional writing\nKeyword integration\nProofreading\n2 revisions included',
            'is_recommended': False,
            'display_order': 6,
        },
        {
            'name': 'logo',
            'description': 'Professional logo design for your brand identity.',
            'price': 1500,
            'billing_cycle': 'once',
            'features': '3 initial concepts\nUnlimited revisions\nSource files included\nMultiple formats\nBrand guidelines',
            'is_recommended': False,
            'display_order': 7,
        },
        {
            'name': 'social',
            'description': 'Social media integration and setup for your website.',
            'price': 800,
            'billing_cycle': 'once',
            'features': 'Social sharing buttons\nFeed integration\nMeta tags setup\nOpen Graph setup\nProfile linking',
            'is_recommended': False,
            'display_order': 8,
        },
        {
            'name': 'analytics',
            'description': 'Google Analytics setup and dashboard configuration.',
            'price': 500,
            'billing_cycle': 'once',
            'features': 'Google Analytics setup\nGoal tracking\nCustom dashboard\nEvent tracking\nMonthly reports setup',
            'is_recommended': True,
            'display_order': 9,
        },
        {
            'name': 'backup',
            'description': 'Automated daily backups with easy restore options.',
            'price': 200,
            'billing_cycle': 'monthly',
            'features': 'Daily backups\n30-day retention\nOne-click restore\nOffsite storage\nEmail notifications',
            'is_recommended': True,
            'display_order': 10,
        },
        {
            'name': 'security',
            'description': 'Advanced security monitoring and protection for your website.',
            'price': 400,
            'billing_cycle': 'monthly',
            'features': 'Malware scanning\nFirewall protection\nDDoS protection\nSecurity alerts\nMonthly security reports',
            'is_recommended': False,
            'display_order': 11,
        },
        {
            'name': 'support',
            'description': 'Priority technical support with faster response times.',
            'price': 300,
            'billing_cycle': 'monthly',
            'features': 'Priority response\n24/7 availability\nPhone support\nRemote assistance\nMonthly check-ins',
            'is_recommended': False,
            'display_order': 12,
        },
    ]
    
    for data in services:
        obj, created = AdditionalService.objects.update_or_create(
            name=data['name'],
            defaults=data
        )
        action = 'Created' if created else 'Updated'
        print(f"{action}: {obj.get_name_display()} - R{obj.price}/{obj.get_billing_cycle_display()}")


if __name__ == '__main__':
    print("Initializing SOFTWAP database data...")
    print("\nCreating Website Types...")
    create_website_types()
    print("\nCreating Additional Services...")
    create_additional_services()
    print("\nInitialization complete!")
