import pytest
from jano.core.src.secured_application import SecuredApplication
import unittest
from jano.core.src.secured_application import SecuredApplication


class TestSecuredApplication(unittest.TestCase):

    def setUp(self):
        self.secured_application = SecuredApplication(
            id_app_proteccion=1,
            name="Test App",
            white_listed_ips="127.0.0.1",
            allow_origin="example.com",
            allow_headers="Content-Type",
            expose_headers="Authorization",
            bus_base_url="https://api.example.com",
            validate_token_ip=True,
            file_queue="/path/to/queue",
            file_repo="/path/to/repo",
            jano_enabled=True,
        )

    def test_secured_application_initialization(self):
        self.assertEqual(self.secured_application.id_app_proteccion, 1)
        self.assertEqual(self.secured_application.name, "Test App")
        self.assertEqual(
            self.secured_application.white_listed_ips, "127.0.0.1")
        self.assertEqual(self.secured_application.allow_origin, "example.com")
        self.assertEqual(
            self.secured_application.allow_headers, "Content-Type")
        self.assertEqual(
            self.secured_application.expose_headers, "Authorization")
        self.assertEqual(self.secured_application.bus_base_url,
                         "https://api.example.com")
        self.assertTrue(self.secured_application.validate_token_ip)
        self.assertEqual(self.secured_application.file_queue, "/path/to/queue")
        self.assertEqual(self.secured_application.file_repo, "/path/to/repo")
        self.assertTrue(self.secured_application.jano_enabled)
