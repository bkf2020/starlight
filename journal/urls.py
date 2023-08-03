from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal, name='journal'),
    path('create/<int:index>/', views.create, name='journal-create')
]