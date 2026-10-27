from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_spaces = models.IntegerField(validators=[MinValueValidator(1)])
    available_spaces = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def save(self, *args, **kwargs):
        if not self.available_spaces:
            self.available_spaces = self.total_spaces
        super().save(*args, **kwargs)

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('CAR', 'Car'),
        ('BIKE', 'Bike'),
        ('TRUCK', 'Truck'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES, default='CAR')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    
    class Meta:
        ordering = ['license_plate']
    
    def __str__(self):
        return f"{self.license_plate} - {self.make} {self.model}"

class ParkingSession(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='parking_sessions')
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='sessions')
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-check_in_time']
    
    def __str__(self):
        return f"{self.vehicle.license_plate} at {self.parking_lot.name}"
    
    def calculate_cost(self):
        if self.check_out_time:
            import datetime
            duration = self.check_out_time - self.check_in_time
            hours = duration.total_seconds() / 3600
            return round(float(self.parking_lot.hourly_rate) * hours, 2)
        return 0
