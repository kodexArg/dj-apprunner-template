from django.test import TestCase
from django.conf import settings
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

class IntegrationTests(TestCase):
    """Suite de pruebas para pruebas de integración a nivel de sistema.
    
    Esta suite verifica la integración entre diferentes componentes del sistema,
    incluyendo configuración del entorno, conectividad de base de datos, servicios AWS,
    y configuraciones de seguridad.
    """

    @classmethod
    def setUpClass(cls):
        """Configura el entorno de prueba para toda la suite de pruebas."""
        super().setUpClass()
    
    def setUp(self):
        """Configura el entorno de prueba para cada test."""
        super().setUp()
    
    def test_environment_configuration(self):
        """Verifica que todas las variables de entorno requeridas estén correctamente configuradas."""
        # Verifica configuración de base de datos
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        
        db_config = settings.DATABASES['default']
        required_db_vars = {
            'DB_HOST': 'HOST',
            'DB_PORT': 'PORT',
            'DB_NAME': 'NAME',
        }
        
        for env_var, db_setting in required_db_vars.items():
            self.assertIn(db_setting, db_config, f"La configuración de base de datos {db_setting} no está configurada")
            self.assertTrue(db_config[db_setting], f"La configuración de base de datos {db_setting} está vacía")
        
        # Verifica configuración de AWS
        required_aws_vars = [
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_REGION_NAME',
            'AWS_S3_CUSTOM_DOMAIN',
        ]
        
        for var in required_aws_vars:
            self.assertTrue(
                hasattr(settings, var),
                f"La configuración de AWS {var} no está configurada"
            )
            self.assertTrue(
                getattr(settings, var),
                f"La configuración de AWS {var} está vacía"
            )

    def test_database_integration(self):
        """Verifica la configuración y ajustes de conectividad de la base de datos."""
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        
        db_config = settings.DATABASES['default']
        required_db_settings = ['ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']
        
        for setting in required_db_settings:
            self.assertIn(setting, db_config)
            self.assertTrue(db_config[setting], f"La configuración de base de datos {setting} está vacía")

    def test_aws_integration(self):
        """Verifica la configuración y ajustes de conectividad de AWS S3."""
        required_s3_settings = [
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_REGION_NAME',
            'AWS_S3_CUSTOM_DOMAIN',
            'AWS_S3_OBJECT_PARAMETERS',
        ]
        
        for setting in required_s3_settings:
            self.assertTrue(
                hasattr(settings, setting),
                f"La configuración de S3 {setting} no está presente"
            )
            self.assertTrue(
                getattr(settings, setting),
                f"La configuración de S3 {setting} está vacía"
            )

    def test_security_integration(self):
        """Verifica la configuración y ajustes relacionados con la seguridad."""
        self.assertFalse(
            settings.DEBUG,
            "DEBUG debe estar deshabilitado en producción"
        )
        
        self.assertTrue(
            hasattr(settings, 'ALLOWED_HOSTS'),
            "ALLOWED_HOSTS no está configurado"
        )
        self.assertTrue(
            isinstance(settings.ALLOWED_HOSTS, (list, tuple)),
            "ALLOWED_HOSTS debe ser una lista o tupla"
        )
        self.assertTrue(
            len(settings.ALLOWED_HOSTS) > 0,
            "ALLOWED_HOSTS está vacío"
        )
        
        aws_domains = ['*.amazonaws.com', '*.apprunner.aws']
        for domain in aws_domains:
            self.assertIn(
                domain,
                settings.ALLOWED_HOSTS,
                f"El dominio {domain} debe estar en ALLOWED_HOSTS"
            )

    def tearDown(self):
        """Limpia después de cada prueba."""
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        """Limpia después de toda la suite de pruebas."""
        super().tearDownClass() 