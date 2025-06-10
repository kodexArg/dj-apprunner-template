from django.test import TestCase
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
import time
from django.db import connection
from django.db.utils import OperationalError
from botocore.config import Config

class PerformanceTests(TestCase):
    """Suite de pruebas para verificar el rendimiento y timeouts."""

    def setUp(self):
        self.timeout_threshold = 5  # segundos

    def test_database_timeout(self):
        """Verifica que las consultas a la base de datos tienen un timeout razonable."""
        start_time = time.time()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.assertEqual(result[0], 1)
                
            execution_time = time.time() - start_time
            self.assertLess(execution_time, self.timeout_threshold)
        except OperationalError as e:
            self.fail(f"Timeout en la base de datos: {str(e)}")

    def test_s3_timeout(self):
        """Verifica que las operaciones S3 tienen un timeout razonable."""
        try:
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                config=Config(connect_timeout=5, read_timeout=5)
            )
            
            start_time = time.time()
            response = s3_client.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                MaxKeys=1
            )
            execution_time = time.time() - start_time
            
            self.assertLess(execution_time, self.timeout_threshold)
            self.assertIsNotNone(response)
        except ClientError as e:
            self.fail(f"Timeout en S3: {str(e)}")

    def test_database_connection_pool(self):
        """Verifica que el pool de conexiones de la base de datos funciona correctamente."""
        try:
            # Intenta crear múltiples conexiones
            for _ in range(5):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    self.assertEqual(result[0], 1)
        except OperationalError as e:
            self.fail(f"Error en el pool de conexiones: {str(e)}")

    def test_s3_connection_pool(self):
        """Verifica que el pool de conexiones S3 funciona correctamente."""
        s3_clients = []
        try:
            # Intenta crear múltiples clientes S3
            for _ in range(5):
                s3_client = boto3.client(
                    's3',
                    region_name=settings.AWS_S3_REGION_NAME
                )
                s3_clients.append(s3_client)
            
            # Verifica que todos los clientes funcionan
            for client in s3_clients:
                response = client.list_objects_v2(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    MaxKeys=1
                )
                self.assertIsNotNone(response)
        except ClientError as e:
            self.fail(f"Error en el pool de conexiones S3: {str(e)}")

    def tearDown(self):
        pass 