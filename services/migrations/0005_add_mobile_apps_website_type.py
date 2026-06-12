from django.db import migrations, models


def add_mobile_apps(apps, schema_editor):
    WebsiteType = apps.get_model('services', 'WebsiteType')
    mobile_apps = [
        ('starter_mobile_app', 'starter-mobile-app', 'A focused mobile app for simple business information and basic service delivery.', 'Android app\nBasic UI design\n3-5 screens\nContact and location details\nApp store deployment', 15000, 25000, 30, 'mobile-alt', 11),
        ('business_mobile_app', 'business-mobile-app', 'A mobile app with user accounts, dashboards, notifications, and database integration.', 'Android and iOS apps\nCustom UI/UX design\nUser accounts\nPush notifications\nDatabase integration', 25000, 60000, 45, 'briefcase', 12),
        ('ecommerce_mobile_app', 'ecommerce-mobile-app', 'A mobile shopping app with products, secure checkout, payments, and order tracking.', 'Product catalogue\nShopping cart and checkout\nPayment integration\nCustomer accounts\nOrder tracking', 45000, 100000, 60, 'shopping-cart', 13),
        ('custom_mobile_app', 'custom-mobile-app', 'A fully custom Android and iOS application built around advanced business requirements.', 'Custom Android and iOS development\nAdvanced integrations\nReal-time features\nAdmin dashboard\nApp store deployment', 60000, 150000, 90, 'rocket', 14),
    ]

    WebsiteType.objects.filter(name='mobile_apps').delete()
    for name, slug, description, features, min_price, max_price, days, icon, order in mobile_apps:
        WebsiteType.objects.update_or_create(
            name=name,
            defaults={
                'slug': slug,
                'description': description,
                'features': features,
                'min_price': min_price,
                'max_price': max_price,
                'estimated_days': days,
                'icon': icon,
                'is_active': True,
                'display_order': order,
            },
        )


def remove_mobile_apps(apps, schema_editor):
    WebsiteType = apps.get_model('services', 'WebsiteType')
    WebsiteType.objects.filter(name__in=[
        'starter_mobile_app',
        'business_mobile_app',
        'ecommerce_mobile_app',
        'custom_mobile_app',
    ]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0004_alter_additionalservice_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websitetype',
            name='name',
            field=models.CharField(
                choices=[
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
                    ('starter_mobile_app', 'Starter Mobile App'),
                    ('business_mobile_app', 'Business Mobile App'),
                    ('ecommerce_mobile_app', 'E-commerce Mobile App'),
                    ('custom_mobile_app', 'Custom Mobile App'),
                ],
                max_length=50,
                unique=True,
            ),
        ),
        migrations.RunPython(add_mobile_apps, remove_mobile_apps),
    ]
