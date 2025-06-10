from django.test import TestCase
from django.conf import settings

class IntegrationTests(TestCase):
    """Suite de pruebas esenciales para verificar configuración y conectividad básica."""

    def setUp(self):
        """Configura el entorno de prueba para cada test."""
        super().setUp()
    
    def test_environment_configuration(self):
        """Verifica que todas las variables de entorno requeridas estén correctamente configuradas."""
        # Verifica SECRET_KEY
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertTrue(settings.SECRET_KEY)
        
        # Verifica configuración de base de datos
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        
        db_config = settings.DATABASES['default']
        required_db_vars = ['HOST', 'PORT', 'NAME']
        
        for db_setting in required_db_vars:
            self.assertIn(db_setting, db_config, f"La configuración de base de datos {db_setting} no está configurada")
            self.assertTrue(db_config[db_setting], f"La configuración de base de datos {db_setting} está vacía")
        
        # Verifica configuración de AWS
        required_aws_vars = [
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_REGION_NAME',
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