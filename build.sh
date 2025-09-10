#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate
# Create superuser automatically
python manage.py createsuperuserauto

# ALWAYS create superuser (since SQLite resets)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')" | python manage.py shell

# Collect static files
python manage.py collectstatic --no-input