from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

class SecurityTests(TestCase):
    """Suite de pruebas para verificar configuraciones básicas de seguridad."""

    def setUp(self):
        self.client = Client()

    def test_csrf_protection(self):
        """Verifica que la protección CSRF está activa."""
        # Verifica que el middleware CSRF está instalado
        self.assertIn(
            'django.middleware.csrf.CsrfViewMiddleware',
            settings.MIDDLEWARE
        )

    def test_authentication_required(self):
        """Verifica que las rutas protegidas requieren autenticación."""
        response = self.client.get(reverse('admin:index'))
        self.assertIn(response.status_code, [302, 403])

    def tearDown(self):
        pass 