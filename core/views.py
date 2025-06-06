from django.http import HttpResponse
import os
from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    """
    Vista principal de la aplicación.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        HttpResponse: Renderiza la plantilla home.html
    """
    return render(request, 'core/home.html')

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
