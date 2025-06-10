#!/bin/bash

set -e  # Stop script if any error occurs

banner() {
  echo ""
  echo "==================================================="
  echo "$1"
  echo "==================================================="
  echo ""
}

banner "[NODE] INICIO DE INSTALACIÓN Y BUILD DE FRONTEND"

banner "[NODE] Instalando Node.js 20.x..."
export NODE_VERSION=20.13.1
export NODE_DIST=node-v$NODE_VERSION-linux-x64
export NODE_PATH=$PWD/.node
if [ ! -d "$NODE_PATH" ]; then
  mkdir -p "$NODE_PATH"
  curl -fsSL https://nodejs.org/dist/v$NODE_VERSION/$NODE_DIST.tar.xz -o $NODE_DIST.tar.xz
  tar -xf $NODE_DIST.tar.xz -C "$NODE_PATH" --strip-components=1
  rm $NODE_DIST.tar.xz
fi
export PATH="$NODE_PATH/bin:$PATH"
echo "[NODE] Node.js versión: $(node -v)"
echo "[NODE] npm versión: $(npm -v)"

banner "[NODE] Instalando dependencias npm..."
if npm ci; then
  echo "[NODE] Dependencias instaladas con npm ci."
else
  echo "[NODE] npm ci falló, intentando con npm install..."
  if npm install; then
    echo "[NODE] Dependencias instaladas con npm install."
  else
    echo "[NODE][ERROR] Falló la instalación de dependencias npm. Abortando."
    exit 1
  fi
fi

banner "[NODE] Ejecutando build de Vite..."
if npm run build; then
  echo "[NODE] Build de Vite completado con éxito."
else
  echo "[NODE][ERROR] Falló el build de Vite. Abortando."
  exit 1
fi

echo "[NODE] Archivos generados en static/dist:"
ls -l static/dist || echo "[NODE] No se encontró static/dist"

banner "[NODE] FIN DE BLOQUE NODE/VITE"

banner "[DJANGO] Migraciones de base de datos"
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