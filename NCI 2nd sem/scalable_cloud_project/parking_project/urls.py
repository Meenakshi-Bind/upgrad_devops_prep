"""parking_project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from parking import views
from parking.views import generate_pdf, check_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Vehicle URLs
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/new/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # Parking URLs
    path('parking-lots/', views.parking_lot_list, name='parking_lot_list'),
    path('parking/start/', views.start_parking, name='start_parking'),
    path('parking/<int:pk>/end/', views.end_parking, name='end_parking'),
    path('parking/history/', views.parking_history, name='parking_history'),
    path('api/pdf/', generate_pdf, name='generate_pdf'),
    path('api/check/', check_api, name='check_api')
]
