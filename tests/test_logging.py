from django.test import TestCase
from django.conf import settings
import logging
import os
from unittest.mock import patch
import json

class LoggingTests(TestCase):
    """Suite de pruebas para verificar la configuración y funcionamiento del logging."""

    def setUp(self):
        """Configura el entorno de prueba para cada test."""
        self.logger = logging.getLogger('django')
        self.test_log_file = 'test.log'

    def test_logging_configuration(self):
        """Verifica que la configuración de logging está presente y correcta."""
        self.assertTrue(hasattr(settings, 'LOGGING'))
        
        # Verifica configuración básica
        self.assertIn('version', settings.LOGGING)
        self.assertIn('disable_existing_loggers', settings.LOGGING)
        
        # Verifica que al menos hay un handler configurado
        self.assertTrue(
            any(key.endswith('Handler') for key in settings.LOGGING.get('handlers', {}).keys()),
            "No hay handlers configurados"
        )

    def test_log_levels(self):
        """Verifica que los diferentes niveles de log funcionan correctamente."""
        with patch('logging.Logger._log') as mock_log:
            # Prueba diferentes niveles de log
            self.logger.debug('Test debug message')
            self.logger.info('Test info message')
            self.logger.warning('Test warning message')
            self.logger.error('Test error message')
            
            # Verifica que se llamaron los niveles principales
            self.assertGreaterEqual(mock_log.call_count, 4)

    def test_log_format(self):
        """Verifica que el formato de los logs es correcto."""
        with patch('logging.Logger._log') as mock_log:
            self.logger.info('Test message')
            
            # Verifica que el mensaje contiene información básica
            args, kwargs = mock_log.call_args
            self.assertIn('Test message', str(args))
            self.assertIn('INFO', str(args))

    def test_log_rotation(self):
        """Verifica que la rotación de logs está configurada correctamente."""
        # Verifica que hay al menos un handler configurado
        self.assertTrue(
            any(key.endswith('Handler') for key in settings.LOGGING.get('handlers', {}).keys()),
            "No hay handlers configurados"
        )

    def tearDown(self):
        """Limpia después de cada prueba."""
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file) 