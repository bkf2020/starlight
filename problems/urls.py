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
    path('cluster/', views.view_cluster, name='view-cluster'),
    path('problemsSimilarInsights/', views.problems_similar_insights, name='problems-similar-insights'),
    path('sharedInsights/', views.shared_insights, name='shared-insights'),
    path('viewAllSummary/', views.view_all_summary, name='view-all-summary'),
    path('viewAllHI/', views.view_all_hints_insights, name='view-all-hints-insights'),
    path('collection/<slug:slug>/', views.view_collection, name='problems-collection'),
]
