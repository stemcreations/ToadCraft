from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('project/<str:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('upload_images/<int:project_id>/', views.upload_images, name='upload_images'),
    path('login/', views.admin_login, name='login_page'),
    path('logout/' , views.logoutUser, name='logout'),

    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_panel/projects/', views.admin_panel_projects, name='admin_projects'),
    path('admin_panel/project_types/', views.admin_project_types, name='admin_project_types'),
    path('admin_panel/project_images/', views.admin_images, name='admin_images'),
    path('admin_panel/project_details/<str:pk>/', views.admin_project_details, name='admin_project_detail'),

    path('admin_panel/customers/', views.admin_customers, name='admin_customers'),
]