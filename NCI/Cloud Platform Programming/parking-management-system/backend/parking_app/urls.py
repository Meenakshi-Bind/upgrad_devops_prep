from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('check-in/', views.check_in_vehicle, name='check_in'),
    path('vehicles/', views.get_all_vehicles, name='get_all_vehicles'),
    path('vehicles/parked/', views.get_parked_vehicles, name='get_parked_vehicles'),
    path('check-out/', views.check_out_vehicle, name='check_out'),
    path('vehicles/<str:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
]