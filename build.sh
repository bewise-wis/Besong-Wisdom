#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create superuser if it doesn't exist (simple Python one-liner)
python -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'wisdombesong123@gmail.com')
password = os.environ.get('SUPERUSER_PASSWORD', 'adminpassword123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
"

# Collect static files
python manage.py collectstatic --no-input