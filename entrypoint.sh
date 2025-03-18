#!/bin/sh

# Apply migrations
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn blog.wsgi:application --bind 0.0.0.0:8000