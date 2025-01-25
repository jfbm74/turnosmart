from django.test import TestCase, Client


class SwaggerEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_swagger_endpoint(self):
        """Test para verificar que la URL de Swagger responde correctamente."""
        response = self.client.get("/swagger/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<div id=\"swagger-ui\">", response.content.decode("utf-8"))  # Verifica el elemento de Swagger

    def test_redoc_endpoint(self):
        """Test para verificar que la URL de ReDoc responde correctamente."""
        response = self.client.get("/redoc/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<div id=\"redoc-placeholder\">", response.content.decode("utf-8"))  # Verifica el elemento de ReDoc
