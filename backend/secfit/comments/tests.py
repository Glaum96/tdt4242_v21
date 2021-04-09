from django.test import TestCase
from rest_framework.test import APIClient
import json
from workouts.models import Workout
from users.models import User
from django.utils import timezone

class CommentsTestCase(TestCase):

    def setUp(self):
        User.objects.create(id="1",username="Bill",password="secret", email="hei")
        self.user_1 = User.objects.get(id="1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.commentURL = "http://testserver/api/comments/"
        self.workout1URL = "http://testserver/api/workouts/1/"

    def testPUComment(self):
        Workout.objects.create(id="1",name="workout",date=timezone.now(),owner=self.user_1, visibility="PU")
        post = self.client.post(self.commentURL,({"workout":self.workout1URL,"content":"asd"}),format='json')
        self.assertEquals(post.status_code,201)

    def testGetComments(self):
        Workout.objects.create(id="1",name="workout",date=timezone.now(),owner=self.user_1, visibility="PU")
        post = self.client.post(self.commentURL,({"workout":self.workout1URL,"content":"asd"}),format='json')
        self.assertEquals(post.status_code,201)
        get = self.client.get("http://testserver/api/comments/")
        datadict = dict(get.data)
        self.assertEquals(len(datadict["results"]), 1)