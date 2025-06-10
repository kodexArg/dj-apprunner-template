#!/bin/bash

set -e  # Stop script if any error occurs

banner() {
  echo ""
  echo "==================================================="
  echo "$1"
  echo "==================================================="
  echo ""
}

banner "FRONTEND BUILD PROCESS"
export NODE_VERSION=20.13.1
export NODE_DIST=node-v$NODE_VERSION-linux-x64
export NODE_PATH=$PWD/.node

sudo yum install -y tar xz-utils
curl -fsSL https://nodejs.org/dist/v$NODE_VERSION/$NODE_DIST.tar.xz -o $NODE_DIST.tar.xz
tar -xf $NODE_DIST.tar.xz -C "$NODE_PATH" --strip-components=1
export PATH="$NODE_PATH/bin:$PATH"

npm install --prefix frontend
npm run build --prefix frontend

banner "DJANGO MIGRATIONS"
.venv/bin/python manage.py makemigrations
.venv/bin/python manage.py migrate

banner "STATIC FILES"
.venv/bin/python manage.py collectstatic --noinput

banner "SUPERUSER CHECK"
.venv/bin/python manage.py createsuperuser --noinput

banner "TESTS"
.venv/bin/python manage.py test tests --verbosity 2
.venv/bin/python manage.py test core.tests.test_views --verbosity 2
.venv/bin/python manage.py test core.tests.test_models --verbosity 2

banner "STARTING GUNICORN"
exec .venv/bin/gunicorn -b 0.0.0.0:8080 project.wsgi --log-level info --access-logfile - --error-logfile - 