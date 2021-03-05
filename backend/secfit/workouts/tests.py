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
from workouts.permissions import *
from django.utils import timezone

# Create your tests here.
"""
Tests for ./permissions.py
"""
class IsOwnerTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        User.objects.create(id="2",username="Alice",password="supersecret")

        self.user_1 = User.objects.get(id="1")
        self.user_2 = User.objects.get(id="2")

        Workout.objects.create(id="1",name="workout",date=timezone.now(),owner=self.user_1,visibility="PR")
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

        request_1.user = self.user_1
        request_2.user = self.user_2

        #Asserting that the owner of the workout (user 1) gets access and that others do not
        self.assertTrue(request_1.status_code == 200) 
        self.assertTrue(request_2.status_code == 403)

        #Formating the response data
        response_data_1 = json.loads(json.dumps(request_1.data))

        #(This is a bit overkill, but still shows the functionality) Asserting that the owner of the fetched workout is user 1, which created the workout in the setup method.
        self.assertEqual(response_data_1["owner"], "http://testserver/api/users/"+str(self.user_1.id)+"/")        
        self.assertNotEqual(response_data_1["owner"], "http://testserver/api/users/"+str(self.user_2.id)+"/")
        
        #Asserting that the function works as it should by returning true if the owner is the one sending the request, and false if it is someone else.
        self.assertTrue(IsOwner.has_object_permission(self,request_1,None,self.workout))
        self.assertFalse(IsOwner.has_object_permission(self,request_2,None,self.workout))

    def tearDown(self):
        return super().tearDown()

class IsOwnerOfWorkoutTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        User.objects.create(id="2",username="Alice",password="supersecret")

        self.user_1 = User.objects.get(id="1")
        self.user_2 = User.objects.get(id="2")

        Workout.objects.create(id="1",name="workout",date=timezone.now(),owner=self.user_1)
        self.workout = Workout.objects.get(name="workout")

        self.client_1 = APIClient()
        self.client_2 = APIClient()

    def test_has_permission(self):
        self.client_1.login(username="Bill", password="secret")
        self.client_2.login(username="Alice", password="supersecret")

        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

        #Disse må kanskje endres når vi setter de inn i CI.
        get_request_1 = self.client_1.get("http://testserver/api/workouts/1/")
        get_request_2 = self.client_2.get("http://testserver/api/workouts/1/")
        post_request_1 = self.client_1.post("http://testserver/api/workouts/",{\
            'name':'myworkout', 'date':timezone.now(), 'notes':'qwerty', 'exercise_instances':[], 'visbility':'PR'},format='json')
        post_request_2 = self.client_2.post("http://testserver/api/workouts/",{},format='json')
        
        get_request_1.user = self.user_1
        get_request_2.user = self.user_2
        post_request_1.user = self.user_1
        post_request_2.user = self.user_2

        get_request_1.method = "GET"
        get_request_2.method = "GET"
        post_request_1.method = "POST"
        post_request_2.method = "POST"

        post_request_1.data["workout"] = post_request_1.data['url']

        self.assertEqual(post_request_1.status_code,201)
        self.assertEqual(post_request_2.status_code,400)

        self.assertTrue(IsOwnerOfWorkout.has_permission(self,get_request_1,None))
        self.assertFalse(IsOwnerOfWorkout.has_permission(self,post_request_2,None))
        self.assertTrue(IsOwnerOfWorkout.has_permission(self,post_request_1,None))

    def test_has_object_permission(self):
        self.client_1.login(username="Bill", password="secret")
        self.client_2.login(username="Alice", password="supersecret")

        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

        #Disse må kanskje endres når vi setter de inn i CI.
        request_1 = self.client_1.get("http://testserver/api/workouts/1/")
        request_2 = self.client_2.get("http://testserver/api/workouts/1/")

        request_1.user = self.user_1
        request_2.user = self.user_2

        #Asserting that the owner of the workout (user 1) gets access and that others do not
        self.assertTrue(request_1.status_code == 200) 
        self.assertTrue(request_2.status_code == 403)

        #Dummy class to place workout inside object
        class WorkOutClass:
            def __init__(self,workout):
                self.workout = workout
                        
        workout_obj = WorkOutClass(self.workout)
        
        #Asserting that the function works as it should by returning true if the owner is the one sending the request, and false if it is someone else.
        self.assertTrue(IsOwnerOfWorkout.has_object_permission(self,request_1,None,workout_obj))
        self.assertFalse(IsOwnerOfWorkout.has_object_permission(self,request_2,None,workout_obj))

    def tearDown(self):
        return super().tearDown()

class IsCoachAndVisibleToCoachTestCase(TestCase):
    def setUp(self):
        pass

    def test_has_object_permission(self):
        pass

    def tearDown(self):
        return super().tearDown()