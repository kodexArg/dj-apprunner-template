from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import re

class SecurityTests(TestCase):
    """Suite de pruebas para verificar configuraciones y comportamientos de seguridad."""

    def setUp(self):
        self.client = Client()

    def test_csrf_protection(self):
        """Verifica que la protección CSRF está activa."""
        # Verifica que el middleware CSRF está instalado
        self.assertIn(
            'django.middleware.csrf.CsrfViewMiddleware',
            settings.MIDDLEWARE
        )

    def test_security_headers(self):
        """Verifica que los headers de seguridad están presentes."""
        response = self.client.get(reverse('hello_world'))
        
        # Verifica headers de seguridad esenciales
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)
        
        # Verifica valores específicos
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')

    def test_authentication_required(self):
        """Verifica que las rutas protegidas requieren autenticación."""
        protected_urls = [
            reverse('admin:index'),
            # Agregar más URLs protegidas aquí
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [302, 403])

    def test_password_policy(self):
        """Verifica que la política de contraseñas es estricta."""
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        
        # Prueba contraseña débil
        weak_passwords = [
            '123456',
            'password',
            'abc123',
        ]
        
        for password in weak_passwords:
            with self.assertRaises(ValidationError):
                validate_password(password)

    def test_session_security(self):
        """Verifica la configuración de seguridad de sesiones."""
        # Verifica configuraciones básicas de seguridad
        self.assertTrue(hasattr(settings, 'SESSION_COOKIE_SECURE'))
        self.assertTrue(hasattr(settings, 'CSRF_COOKIE_SECURE'))

    def tearDown(self):
        pass 