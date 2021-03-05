"""
Tests for the workouts application.
"""
from django.test import TestCase

# Create your tests here.
class TestTestCase(TestCase):

    def test_true(self):
        """Check if true is true"""
        self.assertTrue(True)

        
    def test_false(self):
        """Check if false is false"""
        self.assertFalse(False)