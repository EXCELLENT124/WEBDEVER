from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('services/', views.services_overview_view, name='services_overview'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('place-order/', views.place_order_view, name='place_order'),   # <-- add this line
]
