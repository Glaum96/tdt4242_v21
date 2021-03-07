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
        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

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
        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

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
        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

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
        User.objects.create(id="1",username="Bill",password="secret")
        User.objects.create(id="2",username="Alice",password="supersecret")

        self.user_1 = User.objects.get(id="1")
        self.user_2 = User.objects.get(id="2")

        #Sets up Bill to be Alice's coach but not Allice to be Bill's coach
        self.user_2.coach = self.user_1

        Workout.objects.create(id="1",name="Bill's workout",date=timezone.now(),owner=self.user_1,visibility="CO")
        Workout.objects.create(id="2",name="Allice's workout",date=timezone.now(),owner=self.user_2,visibility="CO")
        self.workout_1 = Workout.objects.get(name="Bill's workout")
        self.workout_2 = Workout.objects.get(name="Allice's workout")
        self.workout_2.owner.coach = self.user_1

        Workout.objects.create(id="3",name="Bill's public workout",date=timezone.now(),owner=self.user_1,visibility="PU")
        Workout.objects.create(id="4",name="Allice's public workout",date=timezone.now(),owner=self.user_2,visibility="PU")
        self.workout_3 = Workout.objects.get(name="Bill's public workout")
        self.workout_4 = Workout.objects.get(name="Allice's public workout")

        self.client_1 = APIClient()
        self.client_2 = APIClient()

    def test_has_object_permission(self):
        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

        request_1 = self.client_1.get("http://testserver/api/workouts/2/")
        request_2 = self.client_2.get("http://testserver/api/workouts/1/")

        request_3 = self.client_1.get("http://testserver/api/workouts/4/")
        request_4 = self.client_2.get("http://testserver/api/workouts/3/")

        request_1.user = self.user_1
        request_2.user = self.user_2
        request_3.user = self.user_1
        request_4.user = self.user_2

        #Bill, who is Allice's coach and sends request 1 for workout 2 (Alice's workout) should receive access
        self.assertTrue(IsCoachAndVisibleToCoach.has_object_permission(self,request_1,None,self.workout_2))
        #Allice should not be able to see Bill's workout since she is not Bill's coach
        self.assertFalse(IsCoachAndVisibleToCoach.has_object_permission(self,request_2,None,self.workout_1))

        #Both of the public workouts should be available
        self.assertEqual(request_3.status_code,200)
        self.assertEqual(request_4.status_code,200)

    def tearDown(self):
        return super().tearDown()

class IsCoachOfOwrkoutAndVisibleToCoachTestCase(TestCase):
    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        User.objects.create(id="2",username="Alice",password="supersecret")

        self.user_1 = User.objects.get(id="1")
        self.user_2 = User.objects.get(id="2")

        #Sets up Bill to be Alice's coach but not Allice to be Bill's coach
        self.user_2.coach = self.user_1

        Workout.objects.create(id="1",name="Bill's workout",date=timezone.now(),owner=self.user_1,visibility="CO")
        Workout.objects.create(id="2",name="Allice's workout",date=timezone.now(),owner=self.user_2,visibility="CO")
        self.workout_1 = Workout.objects.get(name="Bill's workout")
        self.workout_2 = Workout.objects.get(name="Allice's workout")
        self.workout_2.owner.coach = self.user_1

        self.client_1 = APIClient()
        self.client_2 = APIClient()

    def test_has_object_permission(self):
        self.client_1.force_authenticate(user=self.user_1)
        self.client_2.force_authenticate(user=self.user_2)  

        request_1 = self.client_1.get("http://testserver/api/workouts/2/")
        request_2 = self.client_2.get("http://testserver/api/workouts/1/")

        request_3 = self.client_1.get("http://testserver/api/workouts/4/")
        request_4 = self.client_2.get("http://testserver/api/workouts/3/")

        request_1.user = self.user_1
        request_2.user = self.user_2

        class WorkOutClass:
            def __init__(self,workout):
                self.workout = workout
                        
        workout_obj_1 = WorkOutClass(self.workout_1)
        workout_obj_2 = WorkOutClass(self.workout_2)

        #Bill, who is Allice's coach and sends request 1 for workout 2 (Alice's workout) should receive access
        self.assertTrue(IsCoachOfWorkoutAndVisibleToCoach.has_object_permission(self,request_1,None,workout_obj_2))
        #Allice should not be able to see Bill's workout since she is not Bill's coach
        self.assertFalse(IsCoachOfWorkoutAndVisibleToCoach.has_object_permission(self,request_2,None,workout_obj_1))

    def tearDown(self):
        return super().tearDown()

class IsPublicTestCase(TestCase):
    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")

        Workout.objects.create(id="1",name="Bill's public workout",date=timezone.now(),owner=self.user_1,visibility="PU")
        Workout.objects.create(id="2",name="Bill's workout",date=timezone.now(),owner=self.user_1,visibility="CO")
        Workout.objects.create(id="3",name="Bill's private workout",date=timezone.now(),owner=self.user_1,visibility="PR")
        self.workout_1 = Workout.objects.get(name="Bill's public workout")
        self.workout_2 = Workout.objects.get(name="Bill's workout")
        self.workout_3 = Workout.objects.get(name="Bill's private workout")

        self.client_1 = APIClient()

    def test_has_object_permission(self):
        self.client_1.force_authenticate(user=self.user_1)

        request_1 = self.client_1.get("http://testserver/api/workouts/1/")
        request_2 = self.client_1.get("http://testserver/api/workouts/2/")
        request_3 = self.client_1.get("http://testserver/api/workouts/2/")

        request_1.user = self.user_1
        request_2.user = self.user_1
        request_3.user = self.user_1


        #Bill, who is Allice's coach and sends request 1 for workout 2 (Alice's workout) should receive access
        self.assertTrue(IsPublic.has_object_permission(self,request_1,None,self.workout_1))
        self.assertFalse(IsPublic.has_object_permission(self,request_2,None,self.workout_2))
        self.assertFalse(IsPublic.has_object_permission(self,request_3,None,self.workout_3))

    def tearDown(self):
        return super().tearDown()

class IsWorkoutPublicTestCase(TestCase):
    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")

        Workout.objects.create(id="1",name="Bill's workout",date=timezone.now(),owner=self.user_1,visibility="PU")
        Workout.objects.create(id="2",name="Bill's public workout",date=timezone.now(),owner=self.user_1,visibility="CO")
        Workout.objects.create(id="3",name="Bill's private workout",date=timezone.now(),owner=self.user_1,visibility="PR")
        
        self.workout_1 = Workout.objects.get(name="Bill's workout")
        self.workout_2 = Workout.objects.get(name="Bill's public workout")
        self.workout_3 = Workout.objects.get(name="Bill's private workout")


        self.client_1 = APIClient()

    def test_has_object_permission(self):
        self.client_1.force_authenticate(user=self.user_1)

        request_1 = self.client_1.get("http://testserver/api/workouts/1/")
        request_2 = self.client_1.get("http://testserver/api/workouts/2/")
        request_3 = self.client_1.get("http://testserver/api/workouts/2/")


        request_1.user = self.user_1
        request_2.user = self.user_1
        request_3.user = self.user_1


        class WorkOutClass:
            def __init__(self,workout):
                self.workout = workout
                        
        workout_obj_1 = WorkOutClass(self.workout_1)
        workout_obj_2 = WorkOutClass(self.workout_2)
        workout_obj_3 = WorkOutClass(self.workout_3)


        #The first
        self.assertTrue(IsWorkoutPublic.has_object_permission(self,request_1,None,workout_obj_1))
        self.assertFalse(IsWorkoutPublic.has_object_permission(self,request_2,None,workout_obj_2))
        self.assertFalse(IsWorkoutPublic.has_object_permission(self,request_3,None,workout_obj_3))

    def tearDown(self):
        return super().tearDown()

class IsReadOnlyTestCase(TestCase):
    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret")
        self.user_1 = User.objects.get(id="1")

        Workout.objects.create(id="1",name="Bill's public workout",date=timezone.now(),owner=self.user_1,visibility="PU")
        self.workout_1 = Workout.objects.get(name="Bill's public workout")

        self.client_1 = APIClient()

    def test_has_object_permission(self):
        self.client_1.force_authenticate(user=self.user_1)

        get_request = self.client_1.get("http://testserver/api/workouts/1/")
        head_request = self.client_1.head("http://testserver/api/workouts/1/")
        options_request = self.client_1.options("http://testserver/api/workouts/1/")
        put_request = self.client_1.post("http://testserver/api/workouts/",{\
            'name':'myeditedworkout', 'date':timezone.now(), 'notes':'QWERTY', 'exercise_instances':[], 'visbility':'PR'},format='json')
        post_request = self.client_1.post("http://testserver/api/workouts/",{\
            'name':'myworkout', 'date':timezone.now(), 'notes':'qwerty', 'exercise_instances':[], 'visbility':'PR'},format='json')
        delete_request = self.client_1.delete("http://testserver/api/workouts/2/")

        get_request.method = get_request.request.get("REQUEST_METHOD")
        head_request.method = head_request.request.get("REQUEST_METHOD")
        options_request.method = options_request.request.get("REQUEST_METHOD")
        put_request.method = put_request.request.get("REQUEST_METHOD")
        post_request.method = post_request.request.get("REQUEST_METHOD")
        delete_request.method = delete_request.request.get("REQUEST_METHOD")
        
        #Checks that GET, HEAD and OPTIONS requests return true.
        self.assertTrue(IsReadOnly.has_object_permission(self,get_request,None,None))
        self.assertTrue(IsReadOnly.has_object_permission(self,head_request,None,None))
        self.assertTrue(IsReadOnly.has_object_permission(self,options_request,None,None))
        
        #Checks that PUT, POST and DELETE requests fail this permission
        self.assertFalse(IsReadOnly.has_object_permission(self,put_request,None,None))
        self.assertFalse(IsReadOnly.has_object_permission(self,post_request,None,None))
        self.assertFalse(IsReadOnly.has_object_permission(self,delete_request,None,None))

    def tearDown(self):
        return super().tearDown()