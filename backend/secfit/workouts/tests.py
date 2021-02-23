"""
Tests for the workouts application.
"""
from django.test import TestCase
from workouts.models import Workout

# Create your tests here.
"""
Tests for ./permissions.py
"""
class IsOwnerTestCase(TestCase):

    def setUp(self):
        #Workout.objects.create(name="testworkout")
        #testworkout = Workout.objects.get
        return super().setUp()

    def test_has_object_permission(self):
        self.assertEqual(True,True)
    

    
