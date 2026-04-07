#!/bin/bash
# Vercel build script for Django

# Install dependencies (handled by Vercel automatically)
# python -m pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
