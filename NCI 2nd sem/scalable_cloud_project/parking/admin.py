from django.contrib import admin
from .models import ParkingLot, Vehicle, ParkingSession

@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_spaces', 'available_spaces', 'hourly_rate')
    list_filter = ('location',)
    search_fields = ('name', 'location')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'owner', 'vehicle_type', 'make', 'model')
    list_filter = ('vehicle_type',)
    search_fields = ('license_plate', 'owner__username')

@admin.register(ParkingSession)
class ParkingSessionAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'parking_lot', 'check_in_time', 'check_out_time', 'status', 'total_cost')
    list_filter = ('status', 'parking_lot')
    search_fields = ('vehicle__license_plate', 'parking_lot__name')
