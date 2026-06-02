from django.urls import path
from . import views

urlpatterns = [
    # ==============================
    # WEBSITE APPLICATION (DEFAULT)
    # ==============================
    path('', views.apply_view, name='apply'),

    # ==============================
    # MOBILE APPLICATION (NEW)
    # ==============================
    path('apply/mobile/', views.apply_mobile_view, name='apply_mobile'),

    # ==============================
    # SUCCESS PAGE
    # ==============================
    path('success/<int:application_id>/', views.application_success_view, name='application_success'),

    # ==============================
    # STATUS + MESSAGES
    # ==============================
    path('status/<int:application_id>/', views.application_status_view, name='application_status'),
]