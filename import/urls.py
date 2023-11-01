from django.urls import path
from . import views

urlpatterns = [
    path('', views.import_view, name='import'),
]