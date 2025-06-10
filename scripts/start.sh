#!/bin/bash

set -e  # Stop script if any error occurs

echo "--- STARTING FRONTEND BUILD PROCESS ---"
echo "Verifying npm installation..."
npm --version
echo "Installing frontend dependencies..."
npm install --prefix frontend
echo "Building frontend assets..."
npm run build --prefix frontend
echo "--- FRONTEND BUILD PROCESS COMPLETE ---"

echo "Running Django migrations..."
.venv/bin/python manage.py makemigrations
.venv/bin/python manage.py migrate

echo "Collecting static files..."
.venv/bin/python manage.py collectstatic --noinput

echo "Checking superuser existence..."
if ! .venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | grep -q "True"; then
    echo "Creating superuser..."
    .venv/bin/python manage.py createsuperuser --noinput
else
    echo "Superuser already exists, skipping creation."
fi

echo "Running tests in order..."

echo "1. Running project tests..."
.venv/bin/python manage.py test tests --verbosity 2
if [ $? -ne 0 ]; then
    echo "Project tests failed. Aborting deployment."
    exit 1
fi
echo "Project tests passed."

echo "2. Running application tests..."
echo "2.1. Running core.views tests..."
.venv/bin/python manage.py test core.tests.test_views --verbosity 2
if [ $? -ne 0 ]; then
    echo "core.views tests failed. Aborting deployment."
    exit 1
fi

echo "2.2. Running core.models tests..."
.venv/bin/python manage.py test core.tests.test_models --verbosity 2
if [ $? -ne 0 ]; then
    echo "core.models tests failed. Aborting deployment."
    exit 1
fi

echo "All application tests passed successfully."

echo "Starting Gunicorn server..."
exec .venv/bin/gunicorn -b 0.0.0.0:8080 project.wsgi --log-level info --access-logfile - --error-logfile - 