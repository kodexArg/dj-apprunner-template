# dj-apprunner-template

Template en construcción para proyectos Django en AWS App Runner, incluyendo integración con RDS (PostgreSQL) y S3 con CloudFront.

## 📋 Estado del Proyecto

### Infraestructura Core ✅
- App Runner configurado con Python 3.11
- Variables de entorno y secretos
- Gunicorn como servidor WSGI
- Gestión de dependencias con uv
- Configuración de IAM roles y políticas
- Secrets Manager configurado

### Servicios AWS ✅
- Secrets Manager con secretos configurados
- RDS (PostgreSQL) con acceso configurado
- S3 + CloudFront con políticas de acceso
- IAM roles y políticas necesarias

### Próximos Pasos 🚧
1. Configuración del Frontend
   - Instalación de django-vite
   - Configuración de Tailwind CSS
   - Integración de HTMX
2. Sistema de Autenticación
   - Implementación de autenticación Django
3. API REST
   - Desarrollo de endpoints
   - Implementación de seguridad JWT

## 📝 Stack Tecnológico

- **Backend**: Python 3.11, Django, Gunicorn
- **Base de datos**: PostgreSQL (RDS)
- **Almacenamiento**: S3 + CloudFront
- **Despliegue**: AWS App Runner
- **Frontend**: Vite, Tailwind, HTMX, Django Components

## 🔧 Configuración Requerida

### IAM Roles y Políticas

El proyecto utiliza el rol de instancia `kdx-django-apprunner-instance-role` con las siguientes políticas:
- `kdx-AlvsVirginiaS3AccessPolicy`
- `kdx-django-apprunner-required-secrets`
- `kdx-Rds-db-free-tier-policy`

### Secrets Manager

Se requieren los siguientes secretos en AWS Secrets Manager:

1. `django-secret-3cNpZN`:
   - DJANGO_SUPERUSER_USERNAME
   - DJANGO_SUPERUSER_EMAIL
   - DJANGO_SUPERUSER_PASSWORD
   - SECRET_KEY

2. `rds!db-b2e1ff83-1545-4806-bd37-df9fd2a3de95`:
   - username
   - password

3. `pingping/secret-VcQsw5`:
   - PING (valor de prueba que devuelve "PONG")

### Política de Acceso a Secrets

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:789650504128:secret:rds!db-b2e1ff83-1545-4806-bd37-df9fd2a3de95-SR96y6",
                "arn:aws:secretsmanager:us-east-1:789650504128:secret:django-secret-3cNpZN",
                "arn:aws:secretsmanager:us-east-1:789650504128:secret:pingping/secret-VcQsw5"
            ]
        }
    ]
}
```

## 📦 Instalación

1. Clonar el repositorio
2. Configurar los secretos en AWS Secrets Manager según la estructura descrita
3. Asegurar que el rol de instancia tenga las políticas necesarias
4. Configurar las variables de entorno en `apprunner.yaml`
5. Desplegar en AWS App Runner

## 🧪 Pruebas Actuales

```
1. Configuración (tests/test_config.py)
   ├── test_secret_key
   ├── test_database_config
   ├── test_aws_config
   ├── test_security_settings
   ├── test_installed_apps
   └── test_middleware

2. Modelos (core/tests/test_models.py)
   ├── test_create_user
   ├── test_create_superuser
   └── test_user_str_representation

3. Vistas (core/tests/test_views.py)
   ├── test_hello_world
   ├── test_health_check
   ├── test_db_health_check_success
   └── test_db_health_check_failure

4. Integración (tests/test_startup.py)
   ├── test_environment_configuration
   ├── test_database_integration
   ├── test_aws_integration
   └── test_security_integration
```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.