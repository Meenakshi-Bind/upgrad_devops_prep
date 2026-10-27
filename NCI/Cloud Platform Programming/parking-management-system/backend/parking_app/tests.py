from django.test import TestCase
from .models import VehicleRepository

class ParkingTestCase(TestCase):
    def setUp(self):
        self.vehicle_repo = VehicleRepository()
    
    def test_vehicle_creation(self):
        vehicle_data = {
            'vehicle_number': 'TEST123',
            'vehicle_type': '4',
            'vehicle_model': 'Toyota',
            'customer_name': 'John Doe',
            'phone_number': '1234567890'
        }
        
        result = self.vehicle_repo.create_vehicle(vehicle_data)
        self.assertIsNotNone(result)
        self.assertEqual(result['vehicle_number'], 'TEST123')
        self.assertEqual(result['status'], 'parked')