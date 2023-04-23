from django.urls import path
from . import views
from .views import HintUpdateView, InsightUpdateView, HintDeleteView, InsightDeleteView

urlpatterns = [
    path('', views.list, name='problems-list'),
    path('<int:index>/', views.problem, name='problems-view'),
    path('hint/<int:pk>/update/', HintUpdateView.as_view(), name='hint-update'),
    path('insight/<int:pk>/update/', InsightUpdateView.as_view(), name='insight-update'),
    path('hint/<int:pk>/delete/', HintDeleteView.as_view(), name='hint-delete'),
    path('insight/<int:pk>/delete/', InsightDeleteView.as_view(), name='insight-delete'),
]