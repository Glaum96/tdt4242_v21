"""
Tests for the workouts application.
"""
from django.test import TestCase
from workouts.models import Workout
from users.models import User
from rest_framework.test import RequestsClient

# Create your tests here.
"""
Tests for ./permissions.py
"""
class IsOwnerTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        User.objects.create(id="2",username="Alice",password="supersecret")
        Workout.objects.create(id="1",name="workout",date="2021-02-23 14:00",owner_id="1")

    def test_has_object_permission(self):
        user_1 = User.objects.get(id="1")
        user_2 = User.objects.get(id="2")
        workout = Workout.objects.get(name="workout")

        client1 = RequestsClient()
        client1.login(username="Bill",password="secret")

        client2 = RequestsClient()
        client2.login(username="Alice",password="supersecret")

        #Disse må fort endres når vi setter de inn i CI.
        request1 = client1.get("/api/workouts/1")
        request2 = client2.get("/api/workouts/1")

        #self.assertEqual(user_1.username,client1.)
        self.assertEqual(request1.client, client1)
        self.assertTrue(workout.owner_id == user_1.id)
        self.assertFalse(workout.owner_id == user_2.id)
    

    
