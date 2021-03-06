"""
Tests for the workouts application.
"""
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import json
from workouts.models import Workout
from users.models import User
from workouts.models import Exercise


# Create your tests here.

# Create your tests here.
class WorkoutsNameBoundaryTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.request = json.loads('{"name": "bob","date": "2021-03-20T13:29:00.000Z","notes": "jj","visibility":"PU","exercise_instances": [],"filename": []}')

    def test_blank_name(self):
        self.request["name"] = ""
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_valid_name(self):
        self.request["name"] = "plank"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)
        
    def test_special_name(self):
        self.request["name"] = "Pla’nk #3"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class WorkoutsDateBoundaryTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.request = json.loads('{"name": "bob","date": "2021-03-20T13:29:00.000Z","notes": "jj","visibility":"PU","exercise_instances": [],"filename": []}')

    def test_blank_date(self):
        self.request["date"] = ""
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)
        
    def test_invalid_date(self):
        self.request["date"] = "2021-22-20T13:29:00.000Z"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_valid_date(self):
        self.request["date"] = "2021-03-20T13:29:00.000Z"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class WorkoutsNotesBoundaryTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.request = json.loads('{"name": "bob","date": "2021-03-20T13:29:00.000Z","notes": "jj","visibility":"PU","exercise_instances": [],"filename": []}')

    def test_blank_notes(self):
        self.request["notes"] = ""
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_valid_notes(self):
        self.request["notes"] = "normal plank"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)
        
    def test_special_notes(self):
        self.request["notes"] = "Pla’nk #3"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class WorkoutsVisibilityBoundaryTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.request = json.loads('{"name": "bob","date": "2021-03-20T13:29:00.000Z","notes": "jj","visibility":"PU","exercise_instances": [],"filename": []}')

    def test_blank_visibility(self):
        self.request["visibility"] = ""
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_invalid_visibility(self):
        self.request["visibility"] = "PA"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)
        
    def test_valid_visibility(self):
        self.request["visibility"] = "PU"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class WorkoutsExerciseBoundaryTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.request = json.loads('{"name": "bob","date": "2021-03-20T13:29:00.000Z","notes": "jj","visibility":"PU","exercise_instances": [],"filename": []}')

    def test_blank_visibility(self):
        self.request["visibility"] = ""
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_invalid_visibility(self):
        self.request["visibility"] = "PA"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)
        
    def test_valid_visibility(self):
        self.request["visibility"] = "PU"
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class WorkoutsExerciseBoundaryTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.client.post('http://testserver/api/exercises/', json.dumps({"name":"test","description":"test","unit":"kilos"}), content_type='application/json')
        self.exercise_object = {"exercise":"http://testserver/api/exercises/1/","number":"1","sets":"1"}
        self.request = json.loads('{"name": "bob","date": "2021-03-20T13:29:00.000Z","notes": "jj","visibility":"PU","exercise_instances": [],"filename": []}')

    def test_blank_exercise_instances(self):
        self.request["exercise_instances"] = []
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_invalid_exercise_instances(self):
        self.request["exercise_instances"] = ["geir"]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_invalid_exercise(self):
        self.exercise_object["exercise"] = "http://testserver/api/exercises/4"
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_valid_exercise(self):
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_blank_exercise(self):
        self.exercise_object["exercise"] = ""
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)
    
    def test_blank_number(self):
        self.exercise_object["sets"] = ""
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_blank_sets(self):
        self.exercise_object["number"] = ""
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_invalid_number(self):
        self.exercise_object["number"] = "g"
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_invalid_sets(self):
        self.exercise_object["sets"] = "g"
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_negative_sets(self):
        self.exercise_object["sets"] = "-1"
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_negative_number(self):
        self.exercise_object["number"] = "-1"
        self.request["exercise_instances"] = [self.exercise_object]
        request = self.client.post('http://testserver/api/workouts/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)