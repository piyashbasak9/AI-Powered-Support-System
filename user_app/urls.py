from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/ask/', views.ask_question, name='ask_question'),
]