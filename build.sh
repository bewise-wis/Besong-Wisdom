#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create superuser (only if it doesn't exist)
echo "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'engineerbesong@gmail.com', 'mypassword')
else:
    print('Superuser already exists.')
" | python manage.py shell

# Collect static files
python manage.py collectstatic --no-input