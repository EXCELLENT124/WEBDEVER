from django.urls import path
from . import views

urlpatterns = [
    path('', views.apply_view, name='apply'),
    path('success/<int:application_id>/', views.application_success_view, name='application_success'),
    path('status/<int:application_id>/', views.application_status_view, name='application_status'),
]
