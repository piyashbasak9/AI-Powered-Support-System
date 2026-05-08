from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.staff_login, name='staff_login'),
    path('dashboard/', views.dashboard, name='staff_dashboard'),
    path('resolve/<str:ticket_id>/', views.resolve_ticket, name='resolve_ticket'),
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
    path('api/create-ticket/', views.api_create_ticket, name='api_create_ticket'),
]