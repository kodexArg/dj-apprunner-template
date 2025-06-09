#!/bin/bash

set -e  # Stop script if any error occurs

echo "Installing frontend dependencies and building assets..."
if ! command -v nvm &> /dev/null
then
    echo "NVM not found, installing..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

nvm install 20
nvm use 20
npm install
npm run build

echo "Frontend build complete."

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