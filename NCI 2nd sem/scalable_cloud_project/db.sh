# 1. Create migrations for the parking app
python manage.py makemigrations core

# 2. Apply ALL migrations (this creates the tables)
python manage.py migrate

# 3. Create a superuser (if you haven't already)
python manage.py createsuperuser --username admin --email admin@example.com --noinput
echo "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('admin123'); u.save()" | python manage.py shell

# 4. Create sample parking lots
python manage.py shell << 'EOF'
from parking.models import ParkingLot

# Create parking lots
lots = [
    {"name": "Downtown Garage", "location": "123 Main St", "total_spaces": 100, "hourly_rate": 5.00},
    {"name": "Shopping Mall", "location": "456 Mall Ave", "total_spaces": 200, "hourly_rate": 3.50},
    {"name": "Airport Parking", "location": "789 Airport Rd", "total_spaces": 500, "hourly_rate": 8.00},
]

for data in lots:
    ParkingLot.objects.create(**data)
    print(f"Created: {data['name']}")

print(f" Created {len(lots)} parking lots")
EOF

# 5. Restart the server and try again
python manage.py runserver
