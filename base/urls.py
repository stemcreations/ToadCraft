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
]