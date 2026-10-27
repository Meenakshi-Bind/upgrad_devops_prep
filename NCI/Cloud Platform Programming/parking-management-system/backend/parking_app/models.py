import boto3
import uuid
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class DynamoDBManager:
    def __init__(self):
        self.table_name = 'ParkingManagement'
        self.dynamodb = boto3.resource('dynamodb')
        self._create_table_if_not_exists()
    
    def _create_table_if_not_exists(self):
        try:
            table = self.dynamodb.Table(self.table_name)
            table.table_status
        except ClientError:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'vehicle_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'vehicle_id',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
    
    def get_table(self):
        return self.dynamodb.Table(self.table_name)

class VehicleRepository:
    def __init__(self):
        self.db_manager = DynamoDBManager()
        self.table = self.db_manager.get_table()
    
    def create_vehicle(self, vehicle_data):
        try:
            vehicle_id = str(uuid.uuid4())
            check_in_time = datetime.now().isoformat()
            
            item = {
                'vehicle_id': vehicle_id,
                'vehicle_number': vehicle_data['vehicle_number'].upper(),
                'vehicle_type': vehicle_data['vehicle_type'],
                'vehicle_model': vehicle_data['vehicle_model'],
                'customer_name': vehicle_data['customer_name'],
                'phone_number': vehicle_data['phone_number'],
                'check_in_time': check_in_time,
                'status': 'parked',
                'created_at': check_in_time
            }
            
            self.table.put_item(Item=item)
            logger.info(f"Vehicle checked in: {vehicle_data['vehicle_number']}")
            return item
            
        except ClientError as e:
            logger.error(f"Error creating vehicle: {e}")
            return None
    
    def get_vehicle_by_number(self, vehicle_number):
        try:
            response = self.table.scan(
                FilterExpression='vehicle_number = :vn',
                ExpressionAttributeValues={':vn': vehicle_number.upper()}
            )
            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Error getting vehicle: {e}")
            return []
    
    def get_all_vehicles(self):
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Error getting all vehicles: {e}")
            return []
    
    def get_parked_vehicles(self):
        try:
            response = self.table.scan(
                FilterExpression='#status = :stat',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':stat': 'parked'}
            )
            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Error getting parked vehicles: {e}")
            return []
    
    def checkout_vehicle(self, vehicle_number):
        try:
            vehicles = self.get_vehicle_by_number(vehicle_number)
            if not vehicles:
                return None
            
            vehicle = next((v for v in vehicles if v.get('status') == 'parked'), None)
            if not vehicle:
                return None
            
            check_in_time = datetime.fromisoformat(vehicle['check_in_time'])
            check_out_time = datetime.now()
            duration_hours = Decimal(str(round((check_out_time - check_in_time).total_seconds() / 3600, 2)))
            cost = Decimal(str(round(float(duration_hours) * 10, 2)))
            
            response = self.table.update_item(
                Key={'vehicle_id': vehicle['vehicle_id']},
                UpdateExpression='SET check_out_time = :cot, duration_hours = :dur, total_cost = :cost, #status = :stat',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':cot': check_out_time.isoformat(),
                    ':dur': duration_hours,
                    ':cost': cost,
                    ':stat': 'checked_out'
                },
                ReturnValues='ALL_NEW'
            )
            
            logger.info(f"Vehicle checked out: {vehicle_number}")
            return response.get('Attributes')
            
        except ClientError as e:
            logger.error(f"Error during checkout: {e}")
            return None
    
    def delete_vehicle(self, vehicle_id):
        try:
            self.table.delete_item(Key={'vehicle_id': vehicle_id})
            logger.info(f"Vehicle deleted: {vehicle_id}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting vehicle: {e}")
            return False