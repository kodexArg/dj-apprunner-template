#!/bin/bash

set -e  # Stop script if any error occurs

echo "--- STARTING FRONTEND BUILD PROCESS ---"
echo "Instalando Node.js 20.x..."

export NODE_VERSION=20.13.1
export NODE_DIST=node-v$NODE_VERSION-linux-x64
export NODE_PATH=$PWD/.node

echo "Instalando dependencias del sistema..."
sudo yum install -y tar xz

echo "Descargando Node.js..."
curl -fsSL https://nodejs.org/dist/v$NODE_VERSION/$NODE_DIST.tar.xz -o $NODE_DIST.tar.xz

echo "Descomprimiendo Node.js..."
tar -xf $NODE_DIST.tar.xz -C "$NODE_PATH" --strip-components=1

echo "Agregando Node.js a PATH..."
export PATH="$NODE_PATH/bin:$PATH"

echo "Verificando instalación de npm..."
if ! command -v npm >/dev/null 2>&1; then
  echo "$(date '+%m-%d-%Y %H:%M:%S %p') [ERROR] npm no está disponible tras instalar Node.js. Abortando."
  exit 1
fi

echo "npm versión: $(npm -v)"
echo "node versión: $(node -v)"

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