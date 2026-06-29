from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/add_member/', views.project_add_member, name='project_add_member'),
    path('<int:pk>/sprint/create/', views.sprint_create, name='sprint_create'),
    path('sprint/<int:pk>/', views.sprint_detail, name='sprint_detail'),
]
