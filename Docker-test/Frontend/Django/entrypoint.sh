#!/bin/bash
# Check for and apply any database migrations
echo "Checking for and applying database migrations..."
python manage.py makemigrations
python manage.py makemigrations monapp
python manage.py migrate

# Populate the database tables from the SQL script
echo "Populating database tables..."
PGPASSWORD=${DJANGO_DB_PASSWORD} psql -h ${DJANGO_DB_HOST} -d ${DJANGO_DB_NAME} -U ${DJANGO_DB_USER} -f populate_db_tables.sql

# Start the Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:80