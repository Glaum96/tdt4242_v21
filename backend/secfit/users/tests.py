from django.test import TestCase

# Create your tests here.
"""
Tests for UserSerializers ./serializers.py
"""

class UserSerializerTestCase(TestCase):

    def setUp(self):
        #password = serializers.CharField(style={"input_type": "password"}, write_only=True)
        #password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)
        pass

    def test_validate_password(self):
        pass

    def test_create(self):
        pass

    def tearDown(self):
        return super().tearDown()