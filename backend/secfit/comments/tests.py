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
        User.objects.create(id="2",username="Bill2",password="secret", email="hei1")
        self.user_2 = User.objects.get(id="2")
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user_2)
        self.commentURL = "http://testserver/api/comments/"
        self.workout1URL = "http://testserver/api/workouts/1/"

    def testPostComment(self):
        Workout.objects.create(id="1",name="workout",date=timezone.now(),owner=self.user_1, visibility="PU")
        post = self.client.post(self.commentURL,({"workout":self.workout1URL,"content":"asd"}),format='json')
        self.assertEquals(post.status_code,201)

    def testGetPublicComments(self):
        Workout.objects.create(id="1",name="workout",date=timezone.now(),owner=self.user_1, visibility="PU")
        post = self.client.post(self.commentURL,({"workout":self.workout1URL,"content":"asd"}),format='json')
        self.assertEquals(post.status_code,201)
        user1get = self.client.get("http://testserver/api/comments/")
        datadict = dict(user1get.data)
        self.assertEquals(len(datadict["results"]), 1)
        user2get = self.client2.get("http://testserver/api/comments/")
        datadict2 = dict(user2get.data)
        self.assertEquals(len(datadict2["results"]), 1)

    def testGetPrivateComments(self):
        Workout.objects.create(id="2",name="workout",date=timezone.now(),owner=self.user_2, visibility="PR")
        self.client2.post(self.commentURL,({"workout":"http://testserver/api/workouts/2/","content":"assdsdd"}),format='json')
        user1get = self.client.get("http://testserver/api/comments/")
        datadict = dict(user1get.data)
        self.assertEquals(len(datadict["results"]), 0)
        user2get = self.client2.get("http://testserver/api/comments/")
        datadict2 = dict(user2get.data)
        self.assertEquals(len(datadict2["results"]), 1)

    def testGetCoachComment(self):
        User.objects.create(id="3",username="Bill3",password="secret", email="hei2", coach=self.user_1)
        self.user_3 = User.objects.get(id="3")
        self.client3 = APIClient()
        self.client3.force_authenticate(user=self.user_3)
        Workout.objects.create(id="3",name="workout",date=timezone.now(),owner=self.user_3, visibility="CO")
        self.client3.post(self.commentURL,({"workout":"http://testserver/api/workouts/3/","content":"asd"}),format='json')
        user1get = self.client.get("http://testserver/api/comments/")
        datadict = dict(user1get.data)
        self.assertEquals(len(datadict["results"]), 1)
        user2get = self.client2.get("http://testserver/api/comments/")
        datadict2 = dict(user2get.data)
        self.assertEquals(len(datadict2["results"]), 0)
