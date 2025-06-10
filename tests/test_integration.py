from django.test import TestCase
from django.conf import settings
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
import os
import subprocess

class IntegrationTests(TestCase):
    """Suite de pruebas para pruebas de integración de servicios externos. Verifica la conectividad y funcionalidad con AWS S3, la base de datos, y herramientas de frontend."""

    @classmethod
    def setUpClass(cls):
        """Configura el entorno de prueba para toda la suite de pruebas."""
        super().setUpClass()
    
    def setUp(self):
        """Configura el entorno de prueba para cada test."""
        super().setUp()

    def test_s3_connectivity(self):
        """Verifica la conectividad real con AWS S3 intentando listar objetos en el bucket."""
        try:
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME
            )
            # Intenta listar objetos en el bucket
            response = s3_client.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                MaxKeys=1
            )
            self.assertIsNotNone(response)
        except ClientError as e:
            self.fail(f"Prueba de conectividad S3 fallida: {str(e)}")

    def test_database_connectivity(self):
        """Verifica la conectividad de la base de datos ejecutando una consulta SELECT simple."""
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.assertEqual(result[0], 1)
        except Exception as e:
            self.fail(f"Prueba de conectividad de base de datos fallida: {str(e)}")

    def test_static_files_storage(self):
        """Verifica el almacenamiento de archivos estáticos en S3 guardando y recuperando un archivo de prueba."""
        from storages.backends.s3boto3 import S3Boto3Storage
        storage = S3Boto3Storage()
        test_content = b"Test content for static file storage"
        content_file = ContentFile(test_content)
        test_filename = "test_static_file.txt"
        
        try:
            # Intenta guardar un archivo
            storage.save(test_filename, content_file)
            
            # Intenta leerlo de vuelta
            with storage.open(test_filename) as f:
                content = f.read()
                self.assertEqual(content, test_content)
            
            # Limpieza
            storage.delete(test_filename)
        except Exception as e:
            self.fail(f"Prueba de almacenamiento de archivos estáticos fallida: {str(e)}")

    def test_node_installation(self):
        """Verifica que Node.js está instalado y accesible."""
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, "Node.js no está instalado o no es accesible")
            self.assertTrue(result.stdout.strip().startswith('v'), "Versión de Node.js no válida")
        except Exception as e:
            self.fail(f"Error al verificar Node.js: {str(e)}")

    def test_vite_dev_server(self):
        """Verifica que el servidor de desarrollo de Vite está configurado correctamente."""
        vite_config_path = os.path.join(settings.BASE_DIR, 'vite.config.js')
        self.assertTrue(os.path.exists(vite_config_path), "El archivo de configuración de Vite no existe")
        
        # Verifica que el archivo de configuración contiene configuraciones esenciales
        with open(vite_config_path, 'r') as f:
            config_content = f.read()
            self.assertIn('server', config_content, "Configuración del servidor de desarrollo no encontrada")
            self.assertIn('build', config_content, "Configuración de build no encontrada")

    def tearDown(self):
        """Limpia después de cada prueba."""
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        """Limpia después de toda la suite de pruebas."""
        super().tearDownClass() 