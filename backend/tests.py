from django.test import TestCase
from .customauthbackend import EmailAuthBackend
from .models import Member

class EmailAuthBackendTestCase(TestCase):
    def setUp(self):
        self.backend = EmailAuthBackend()
        self.user = Member.objects.create(email='test@example.com', password='testpassword')

    def test_authenticate_success(self):
        user = self.backend.authenticate(None, 'test@example.com', 'testpassword')
        self.assertEqual(user, self.user)

    def test_authenticate_failure(self):
        user = self.backend.authenticate(None, 'test@example.com', 'wrongpassword')
        self.assertIsNone(user)