#!/bin/bash
# Check for and apply any database migrations
echo "Checking for and applying database migrations..."
python manage.py makemigrations
python manage.py makemigrations monapp
python manage.py migrate

# Start the Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:80