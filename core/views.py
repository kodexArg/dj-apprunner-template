from django.http import HttpResponse
import os
import sys
import django
from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

def home(request):
    """
    Vista principal de la aplicación con información detallada del sistema.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        HttpResponse: Renderiza la plantilla home.html con información del sistema
    """
    context = {
        'django_version': django.get_version(),
        'python_version': sys.version.split()[0],
        'csrf_enabled': settings.CSRF_COOKIE_SECURE,
        'https_enabled': settings.SECURE_PROXY_SSL_HEADER is not None,
        'debug_mode': settings.DEBUG,
        'storage_backend': 'S3' if not settings.IS_LOCAL else 'Local',
        'cdn_enabled': bool(settings.AWS_S3_CUSTOM_DOMAIN),
        's3_bucket_name': settings.AWS_STORAGE_BUCKET_NAME,
        'environment': 'Desarrollo' if settings.IS_LOCAL else 'Producción',
        'aws_region': settings.AWS_S3_REGION_NAME,
        'server_info': 'Gunicorn' if not settings.IS_LOCAL else 'Django Development Server'
    }
    return render(request, 'core/home.html', context)

def hello_world(request):
    """
    Vista de prueba que devuelve un mensaje simple.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        HttpResponse: Mensaje "Hello World"
    """
    return HttpResponse("Hola Mundo")

def health(request):
    """
    Endpoint de verificación de salud de la aplicación.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        JsonResponse: Estado de la aplicación y mensaje de éxito
    """
    return JsonResponse({'status': 'ok', 'message': 'Verificación de estado exitosa'}, status=200)

def db_health_check(request):
    """
    Verifica la conexión a la base de datos.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        JsonResponse: Estado de la conexión a la base de datos
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return JsonResponse({'status': 'ok', 'message': 'Conexión a la base de datos exitosa'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Error en la conexión a la base de datos'}, status=500)
