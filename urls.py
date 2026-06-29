from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('search/', views.global_search, name='global_search'),
    path('reports/', views.reports_view, name='reports'),
]
