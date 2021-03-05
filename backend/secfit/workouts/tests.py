"""
Tests for the workouts application.
"""
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import json

# Create your tests here.
class RegisterBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "","password": "123","password1": "123","athletes": [],"email": "","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "","country": "","city": "","street_address":""}')
        self.client = APIClient()

    def test_good_username(self):
        self.request["username"] = "bob"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_bad_username(self):
        self.request["username"] = "<<<"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)
        
        


    