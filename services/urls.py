from django.urls import path
from . import views

urlpatterns = [
    path('website-types/', views.website_type_list_view, name='website_type_list'),
    path('website-types/<slug:slug>/', views.website_type_detail_view, name='website_type_detail'),
    path('additional-services/', views.additional_service_list_view, name='additional_service_list'),
    path('additional-services/<slug:slug>/', views.additional_service_detail_view, name='additional_service_detail'),
    path('packages/', views.package_list_view, name='package_list'),
    path('packages/<slug:slug>/', views.package_detail_view, name='package_detail'),
    path('ajax/website-type-price/<int:website_type_id>/', views.get_website_type_price, name='website_type_price_ajax'),
    path('ajax/additional-service-price/<int:service_id>/', views.get_additional_service_price, name='additional_service_price_ajax'),
]
