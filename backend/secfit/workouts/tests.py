"""
Tests for the workouts application.
"""
from django.test import TestCase
from workouts.models import Workout
from users.models import User
from rest_framework.test import RequestsClient
from requests.auth import HTTPBasicAuth
import requests

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

        client_1 = RequestsClient()
        #client_1.auth = HTTPBasicAuth('user', 'pass')
        #print("client_1.headers:\n\n",client_1.headers,"\n\n")
        #client_1.headers.update({'Cookie': 'access=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE0MzI3ODA4LCJqdGkiOiI2N2JmNzQ5YjQ1ZWY0Njg1YTM4MTc1MDMwZTZiNTNiMSIsInVzZXJfaWQiOjJ9.I7hOEFPqmWSgCa7CMa5INmeUhAuerIpBD3ps4WBykZ0; refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDQxMzkwOCwianRpIjoiN2E3ZjQ1ODFhOWQ3NGU4NmE5NWUzYzlhZWIwNTExMWYiLCJ1c2VyX2lkIjoyfQ.FCHh4rKkKr4AhnC_ZGk3dvn3EyJeu7-thhbevD4u9WM'})
        #client_1.headers.update({'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE0MzI3ODA4LCJqdGkiOiI2N2JmNzQ5YjQ1ZWY0Njg1YTM4MTc1MDMwZTZiNTNiMSIsInVzZXJfaWQiOjJ9.I7hOEFPqmWSgCa7CMa5INmeUhAuerIpBD3ps4WBykZ0'})
        #print("client_1.headers:\n\n",client_1.headers,"\n\n")
        
        #client2 = RequestsClient()
        #client2.login(username="Alice",password="supersecret")

        #Disse må fort endres når vi setter de inn i CI.
        request_1 = client_1.get("http://testserver/api/workouts/1/", auth=('Bill','secret'))
        #request2 = client2.get("/api/workouts/1")¨
        #print(request_1.__dict__)

        #self.assertEqual(user_1.username,client1.)
        print("request1.status_code:",request_1.status_code)
        print("request_1:\n\n",request_1.__dict__,"\n\n")
        self.assertTrue(request_1.status_code == 200) 
        #self.assertEqual(request_1.client, client_1)
        self.assertTrue(workout.owner_id == user_1.id)
        self.assertFalse(workout.owner_id == user_2.id)
    

    
