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

echo "1. Running configuration tests..."
.venv/bin/python manage.py test tests/test_config.py --verbosity 2
if [ $? -ne 0 ]; then
    echo "Configuration tests failed. Aborting deployment."
    exit 1
fi
echo "Configuration tests passed."

echo "2. Running startup tests..."
.venv/bin/python manage.py test tests/test_startup.py --verbosity 2
if [ $? -ne 0 ]; then
    echo "Startup tests failed. Aborting deployment."
    exit 1
fi
echo "Startup tests passed."

echo "3. Running integration tests..."
.venv/bin/python manage.py test tests/test_integration.py --verbosity 2
if [ $? -ne 0 ]; then
    echo "Integration tests failed. Aborting deployment."
    exit 1
fi
echo "Integration tests passed."

echo "4. Running application tests..."
echo "4.1. Running core.views tests..."
.venv/bin/python manage.py test core/tests/test_views.py --verbosity 2
if [ $? -ne 0 ]; then
    echo "core.views tests failed. Aborting deployment."
    exit 1
fi

echo "4.2. Running core.models tests..."
.venv/bin/python manage.py test core/tests/test_models.py --verbosity 2
if [ $? -ne 0 ]; then
    echo "core.models tests failed. Aborting deployment."
    exit 1
fi

echo "All application tests passed successfully."

echo "Starting Gunicorn server..."
exec .venv/bin/gunicorn -b 0.0.0.0:8080 project.wsgi --log-level info --access-logfile - --error-logfile - 