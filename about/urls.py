from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about-starlight'),
    path('privacy/', views.privacy, name='about-privacy'),
    path('rules/', views.rules, name='about-rules')
]