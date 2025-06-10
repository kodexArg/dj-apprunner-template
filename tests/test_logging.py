from django.test import TestCase
from django.conf import settings
import logging
import os
from unittest.mock import patch
import json

class LoggingTests(TestCase):
    """Suite de pruebas para verificar la configuración y funcionamiento del logging."""

    def setUp(self):
        self.logger = logging.getLogger('django')
        self.test_log_file = 'test.log'

    def test_logging_configuration(self):
        """Verifica que la configuración de logging está presente y correcta."""
        self.assertTrue(hasattr(settings, 'LOGGING'))
        self.assertIn('handlers', settings.LOGGING)
        self.assertIn('loggers', settings.LOGGING)
        
        # Verifica configuración de handlers
        handlers = settings.LOGGING['handlers']
        self.assertIn('console', handlers)
        self.assertIn('file', handlers)
        
        # Verifica configuración de loggers
        loggers = settings.LOGGING['loggers']
        self.assertIn('django', loggers)
        self.assertIn('django.request', loggers)
        self.assertIn('django.security', loggers)

    def test_log_file_creation(self):
        """Verifica que los archivos de log se crean correctamente."""
        log_dir = os.path.dirname(settings.LOGGING['handlers']['file']['filename'])
        self.assertTrue(os.path.exists(log_dir))
        self.assertTrue(os.access(log_dir, os.W_OK))

    def test_log_levels(self):
        """Verifica que los diferentes niveles de log funcionan correctamente."""
        with patch('logging.Logger._log') as mock_log:
            # Prueba diferentes niveles de log
            self.logger.debug('Test debug message')
            self.logger.info('Test info message')
            self.logger.warning('Test warning message')
            self.logger.error('Test error message')
            self.logger.critical('Test critical message')
            
            # Verifica que se llamaron todos los niveles
            self.assertEqual(mock_log.call_count, 5)

    def test_log_format(self):
        """Verifica que el formato de los logs es correcto."""
        with patch('logging.Logger._log') as mock_log:
            self.logger.info('Test message')
            
            # Obtiene el formato del log
            log_format = settings.LOGGING['formatters']['verbose']['format']
            
            # Verifica que el formato contiene los elementos necesarios
            self.assertIn('%(asctime)s', log_format)
            self.assertIn('%(levelname)s', log_format)
            self.assertIn('%(message)s', log_format)

    def test_log_rotation(self):
        """Verifica que la rotación de logs está configurada correctamente."""
        file_handler = settings.LOGGING['handlers']['file']
        self.assertIn('maxBytes', file_handler)
        self.assertIn('backupCount', file_handler)
        
        # Verifica valores razonables
        self.assertGreater(file_handler['maxBytes'], 0)
        self.assertGreater(file_handler['backupCount'], 0)

    def tearDown(self):
        # Limpia archivos de log de prueba
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file) 