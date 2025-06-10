from django.test import TestCase
from django.conf import settings
import boto3
from botocore.exceptions import ClientError

class IntegrationTests(TestCase):
    """Suite de pruebas para verificar conectividad con servicios externos."""
    
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

    def tearDown(self):
        """Limpia después de cada prueba."""
        super().tearDown() 