from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('project/<str:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
]