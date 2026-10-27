#!/bin/bash


# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    
    # Generate Django secret key
    DJANGO_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
    
    # Generate DB password
    DB_PASSWORD=$(openssl rand -base64 32 2>/dev/null || python -c "import secrets; print(secrets.token_urlsafe(24))")
    
    cat > .env << EOL
# Django Settings
SECRET_KEY=$DJANGO_SECRET
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=parkingdb
DB_USER=parkingadmin
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
EOL
    
    echo ".env file created"
    echo "IMPORTANT: Save these for GitHub Secrets:"
    echo "DJANGO_SECRET_KEY: $DJANGO_SECRET"
    echo "DB_PASSWORD: $DB_PASSWORD"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo " Running migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py shell << EOL
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")
EOL

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
echo "Run: source venv/bin/activate && python manage.py runserver"
echo "Admin: http://localhost:8000/admin (admin/admin123)"
