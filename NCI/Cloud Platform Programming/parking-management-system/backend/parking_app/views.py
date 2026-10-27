from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VehicleRepository
import logging

logger = logging.getLogger(__name__)
vehicle_repo = VehicleRepository()

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username == 'admin' and password == 'admin123':
        return Response({
            'success': True, 
            'message': 'Login successful',
            'user': {'username': username, 'role': 'admin'}
        })
    
    return Response({
        'success': False, 
        'message': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def check_in_vehicle(request):
    try:
        required_fields = ['vehicle_number', 'vehicle_type', 'vehicle_model', 'customer_name', 'phone_number']
        
        for field in required_fields:
            if field not in request.data or not request.data[field]:
                return Response({
                    'success': False, 
                    'message': f'Missing required field: {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        existing_vehicles = vehicle_repo.get_vehicle_by_number(request.data['vehicle_number'])
        parked_vehicles = [v for v in existing_vehicles if v.get('status') == 'parked']
        
        if parked_vehicles:
            return Response({
                'success': False, 
                'message': 'Vehicle is already parked'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle_data = {
            'vehicle_number': request.data['vehicle_number'],
            'vehicle_type': request.data['vehicle_type'],
            'vehicle_model': request.data['vehicle_model'],
            'customer_name': request.data['customer_name'],
            'phone_number': request.data['phone_number']
        }
        
        result = vehicle_repo.create_vehicle(vehicle_data)
        
        if result:
            return Response({
                'success': True, 
                'message': 'Vehicle checked in successfully',
                'data': result
            })
        else:
            return Response({
                'success': False, 
                'message': 'Failed to check in vehicle'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Check-in error: {e}")
        return Response({
            'success': False, 
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_vehicles(request):
    try:
        vehicles = vehicle_repo.get_all_vehicles()
        return Response({
            'success': True, 
            'data': vehicles,
            'count': len(vehicles)
        })
    except Exception as e:
        logger.error(f"Get vehicles error: {e}")
        return Response({
            'success': False, 
            'message': 'Failed to retrieve vehicles'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_parked_vehicles(request):
    try:
        vehicles = vehicle_repo.get_parked_vehicles()
        return Response({
            'success': True, 
            'data': vehicles,
            'count': len(vehicles)
        })
    except Exception as e:
        logger.error(f"Get parked vehicles error: {e}")
        return Response({
            'success': False, 
            'message': 'Failed to retrieve parked vehicles'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def check_out_vehicle(request):
    try:
        vehicle_number = request.data.get('vehicle_number')
        
        if not vehicle_number:
            return Response({
                'success': False, 
                'message': 'Vehicle number is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = vehicle_repo.checkout_vehicle(vehicle_number)
        
        if result:
            return Response({
                'success': True, 
                'message': 'Vehicle checked out successfully',
                'data': result
            })
        else:
            return Response({
                'success': False, 
                'message': 'Vehicle not found or already checked out'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Check-out error: {e}")
        return Response({
            'success': False, 
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_vehicle(request, vehicle_id):
    try:
        if vehicle_repo.delete_vehicle(vehicle_id):
            return Response({
                'success': True, 
                'message': 'Vehicle deleted successfully'
            })
        else:
            return Response({
                'success': False, 
                'message': 'Failed to delete vehicle'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Delete vehicle error: {e}")
        return Response({
            'success': False, 
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)