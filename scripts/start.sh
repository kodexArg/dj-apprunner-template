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

banner "[DJANGO] Collecting static files"
.venv/bin/python manage.py collectstatic --noinput

banner "[DJANGO] Verificando existencia de superusuario"
if ! .venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | grep -q "True"; then
    echo "[DJANGO] Creando superusuario..."
    .venv/bin/python manage.py createsuperuser --noinput
else
    echo "[DJANGO] Superusuario ya existe, omitiendo creación."
fi

banner "[TESTS] Ejecutando pruebas de proyecto"
.venv/bin/python manage.py test tests --verbosity 2
if [ $? -ne 0 ]; then
    echo "[TESTS][ERROR] Pruebas de proyecto fallidas. Abortando despliegue."
    exit 1
fi
banner "[TESTS] Pruebas de proyecto OK"

banner "[TESTS] Ejecutando pruebas de aplicación: core.views"
.venv/bin/python manage.py test core.tests.test_views --verbosity 2
if [ $? -ne 0 ]; then
    echo "[TESTS][ERROR] Pruebas core.views fallidas. Abortando despliegue."
    exit 1
fi
banner "[TESTS] core.views OK"

banner "[TESTS] Ejecutando pruebas de aplicación: core.models"
.venv/bin/python manage.py test core.tests.test_models --verbosity 2
if [ $? -ne 0 ]; then
    echo "[TESTS][ERROR] Pruebas core.models fallidas. Abortando despliegue."
    exit 1
fi
banner "[TESTS] core.models OK"

echo "Todas las pruebas de aplicación pasaron correctamente."

banner "[GUNICORN] Iniciando servidor Gunicorn"
exec .venv/bin/gunicorn -b 0.0.0.0:8080 project.wsgi --log-level info --access-logfile - --error-logfile - 