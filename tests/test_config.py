from django.test import TestCase
from django.conf import settings

class ConfigTests(TestCase):
    """Suite de pruebas para configuraciones críticas."""

    def setUp(self):
        """Configura el entorno de prueba para cada test."""
        super().setUp()

    def test_secret_key(self):
        """Verifica que SECRET_KEY está configurado."""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertTrue(settings.SECRET_KEY)

    def test_database_config(self):
        """Verifica que la configuración de la base de datos está presente."""
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        
        db_config = settings.DATABASES['default']
        required_settings = ['ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']
        
        for setting in required_settings:
            self.assertIn(setting, db_config)
            self.assertTrue(db_config[setting], f"La configuración de base de datos {setting} está vacía")

    def test_aws_config(self):
        """Verifica que la configuración de AWS está presente."""
        required_settings = [
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_REGION_NAME',
        ]
        
        for setting in required_settings:
            self.assertTrue(
                hasattr(settings, setting),
                f"La configuración de AWS {setting} no está presente"
            )
            self.assertTrue(
                getattr(settings, setting),
                f"La configuración de AWS {setting} está vacía"
            )

    def test_security_settings(self):
        """Verifica que la configuración de seguridad está correctamente configurada."""
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

    def tearDown(self):
        """Limpia después de cada prueba."""
        super().tearDown() 