"""
Tests for the workouts application.
"""
from django.test import TestCase
from workouts.models import Workout
from users.models import User
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
import requests
import json

# Create your tests here.
"""
Tests for ./permissions.py
"""
class IsOwnerTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        User.objects.create(id="2",username="Alice",password="supersecret")
        Workout.objects.create(id="1",name="workout",date="2021-02-23 14:00",owner_id="1")

        self.user_1 = User.objects.get(id="1")
        self.user_2 = User.objects.get(id="2")
        self.workout = Workout.objects.get(name="workout")

        self.client_1 = APIClient()
        self.client_2 = APIClient()

    def test_has_object_permission(self):

        self.client_1.login(username="Bill", password="secret")
        self.client_2.login(username="Alice", password="supersecret")

        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

        #Disse må kanskje endres når vi setter de inn i CI.
        request_1 = self.client_1.get("http://testserver/api/workouts/1/")
        request_2 = self.client_2.get("http://testserver/api/workouts/1/")

        #Asserting that the owner of the workout (user 1) gets access and that others do not
        self.assertTrue(request_1.status_code == 200) 
        self.assertTrue(request_2.status_code == 403)

        #Formating the response data
        response_data_1 = json.loads(json.dumps(request_1.data))

        #Asserting that the owner of the fetched workout is user 1, which created the workout in the setup method.
        self.assertEqual(response_data_1["owner"], "http://testserver/api/users/"+str(self.user_1.id)+"/")
        self.assertNotEqual(response_data_1["owner"], "http://testserver/api/users/"+str(self.user_2.id)+"/")

    
