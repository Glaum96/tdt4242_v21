"""Contains views for the workouts application. These are mostly class-based views.
"""
from rest_framework import generics, mixins, permissions, status, filters
from rest_framework.parsers import (
    JSONParser,
)
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q, Sum, F, IntegerField
from workouts.parsers import MultipartJsonParser
from workouts.permissions import (
    IsOwner,
    IsCoachAndVisibleToCoach,
    IsOwnerOfWorkout,
    IsCoachOfWorkoutAndVisibleToCoach,
    IsReadOnly,
    IsPublic,
    IsWorkoutPublic,
)
from workouts.mixins import CreateListModelMixin
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile, WorkoutLike
from workouts.serializers import WorkoutSerializer, ExerciseSerializer, RememberMeSerializer, ExerciseInstanceSerializer, WorkoutFileSerializer
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from collections import namedtuple
import base64, pickle
from django.core.signing import Signer
from users.models import User
from rest_framework.views import APIView


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "workouts": reverse("workout-list", request=request, format=format),
            "exercises": reverse("exercise-list", request=request, format=format),
            "exercise-instances": reverse(
                "exercise-instance-list", request=request, format=format
            ),
            "workout-files": reverse(
                "workout-file-list", request=request, format=format
            ),
            "comments": reverse("comment-list", request=request, format=format),
            "likes": reverse("like-list", request=request, format=format),
        }
    )


# Allow users to save a persistent session in their browser
class RememberMe(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    serializer_class = RememberMeSerializer

    def get(self, request):
        if request.user.is_authenticated == False:
            raise PermissionDenied
        else:
            return Response({"remember_me": self.rememberme()})

    def post(self, request):
        cookie_object = namedtuple("Cookies", request.COOKIES.keys())(
            *request.COOKIES.values()
        )
        user = self.get_user(cookie_object)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )

    def get_user(self, cookie_object):
        decode = base64.b64decode(cookie_object.remember_me)
        user, sign = pickle.loads(decode)

        # Validate signature
        if sign == self.sign_user(user):
            return user

    def rememberme(self):
        creds = [self.request.user, self.sign_user(str(self.request.user))]
        return base64.b64encode(pickle.dumps(creds))

    def sign_user(self, username):
        signer = Signer()
        signed_user = signer.sign(username)
        return signed_user


class WorkoutList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """Class defining the web response for the creation of a Workout, or displaying a list
    of Workouts

    HTTP methods: GET, POST
    """

    serializer_class = WorkoutSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # User must be authenticated to create/view workouts
    parser_classes = [
        MultipartJsonParser,
        JSONParser,
    ]  # For parsing JSON and Multi-part requests
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "date", "owner__username"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = Workout.objects.none()
        if self.request.user:
            # A workout should be visible to the requesting user if any of the following hold:
            # - The workout has public visibility
            # - The owner of the workout is the requesting user
            # - The workout has coach visibility and the requesting user is the owner's coach
            
            # We found that his code has been edited so that private workouts are sent to the frontend if the requesting user is the owner. Otherwise the tests would fail.
            qs = Workout.objects.filter(
                Q(visibility="PU")
                | (Q(visibility="CO") & (Q(owner__coach=self.request.user)) | Q(owner=self.request.user))
                | (Q(visibility="PR") & Q(owner=self.request.user))
            ).distinct()

        return qs


class WorkoutDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Class defining the web response for the details of an individual Workout.

    HTTP methods: GET, PUT, DELETE
    """

    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (IsOwner | (IsReadOnly & (IsCoachAndVisibleToCoach | IsPublic)))
    ]
    parser_classes = [MultipartJsonParser, JSONParser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExerciseList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """Class defining the web response for the creation of an Exercise, or
    a list of Exercises.

    HTTP methods: GET, POST
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExerciseDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Class defining the web response for the details of an individual Exercise.

    HTTP methods: GET, PUT, PATCH, DELETE
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class Leaderboards(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):

        # User must be logged in
        if self.request.user:
    
            leaderboard_numbers = ExerciseInstance.objects.filter(Q(exercise__pk=pk) & Q(workout__visibility='PU')).values('workout__owner__pk').annotate(amount=Sum(F("sets") * F("number"), output_field=IntegerField())).order_by('-amount')
            leaderboard_result = []

            self.addtop5(leaderboard_result, leaderboard_numbers)
            current_logged_in_user = self.request.user
    
            self.adduserscore(current_logged_in_user, leaderboard_result, leaderboard_numbers)

            return Response(leaderboard_result)

    def addtop5(self, leaderboard_result, leaderboard_numbers):
        # Iterates through the top 5 entries in the leaderboard and formats it correctly
        for i in range(0, min(5, len(leaderboard_numbers))):
            leaderboard_result.append({"name": User.objects.get(pk=leaderboard_numbers[i]['workout__owner__pk']).username, "value": leaderboard_numbers[i]['amount']})

            # Applies the rank to the leaderboard entry; if two or more users have the score they get the same rank
            if i > 0 and leaderboard_numbers[i-1]["amount"] == leaderboard_numbers[i]["amount"]:
                leaderboard_result[i]["rank"] = leaderboard_result[i-1]["rank"]
            else:
                leaderboard_result[i]["rank"] = i+1

    def adduserscore(self, current_logged_in_user, leaderboard_result, leaderboard_numbers):
        # Finds the user in the leaderboard list. If the user is not in the leaderboard list,
        # the user is automatically given a score of 0 and the worst rank

        for j in range(0, len(leaderboard_numbers)):
            if leaderboard_numbers[j]['workout__owner__pk'] == current_logged_in_user.pk:
                if j+1 > 5:
                    leaderboard_result.append({"name": current_logged_in_user.username, "value": leaderboard_numbers[j]["amount"], "rank": j+1})
                break
        else:
            leaderboard_result.append({"name": current_logged_in_user.username, "value": 0, "rank": len(leaderboard_numbers) + 1})


class ExerciseInstanceList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):
    """Class defining the web response for the creation"""

    serializer_class = ExerciseInstanceSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfWorkout]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        qs = ExerciseInstance.objects.none()
        if self.request.user:
            qs = ExerciseInstance.objects.filter(
                Q(workout__owner=self.request.user)
                | (
                    (Q(workout__visibility="CO") | Q(workout__visibility="PU"))
                    & Q(workout__owner__coach=self.request.user)
                )
            ).distinct()

        return qs


class ExerciseInstanceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ExerciseInstanceSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (
            IsOwnerOfWorkout
            | (IsReadOnly & (IsCoachOfWorkoutAndVisibleToCoach | IsWorkoutPublic))
        )
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WorkoutFileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutFile.objects.all()
    serializer_class = WorkoutFileSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfWorkout]
    parser_classes = [MultipartJsonParser, JSONParser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = WorkoutFile.objects.none()
        if self.request.user:
            qs = WorkoutFile.objects.filter(
                Q(owner=self.request.user)
                | Q(workout__owner=self.request.user)
                | (
                    Q(workout__visibility="CO")
                    & Q(workout__owner__coach=self.request.user)
                )
            ).distinct()

        return qs


class WorkoutFileDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutFile.objects.all()
    serializer_class = WorkoutFileSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (
            IsOwner
            | IsOwnerOfWorkout
            | (IsReadOnly & (IsCoachOfWorkoutAndVisibleToCoach | IsWorkoutPublic))
        )
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# View for fetching like amount, and for creating new likes
class WorkoutLiking(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Returns a tuple with a boolean value that is true if liking is allowed (the workout does not belong to the user
    # and the workout has not been liked before), and the amount of likes that the workout has
    def get(self, request, pk):

        liking_allowed = Workout.objects.get(pk=pk).owner != self.request.user and WorkoutLike.objects.filter(
            Q(userLiking=self.request.user) & Q(workoutToLike__pk=pk)).count() == 0

        like_amount = WorkoutLike.objects.filter(Q(workoutToLike__pk=pk)).count() + 1

        return Response((liking_allowed, like_amount), status.HTTP_200_OK)

    # Tries to like a new post and returns the same as the GET above
    def post(self, request, pk):

        liking_allowed = Workout.objects.get(pk=pk).owner != self.request.user and WorkoutLike.objects.filter(
            Q(userLiking=self.request.user) & Q(workoutToLike__pk=pk)).count() == 0

        like_amount = WorkoutLike.objects.filter(Q(workoutToLike__pk=pk)).count() + 1

        if liking_allowed:
            new_workout_like = WorkoutLike(workoutToLike=Workout.objects.get(pk=pk), userLiking=self.request.user)
            new_workout_like.save()

            return Response((False, like_amount + 1), status.HTTP_201_CREATED)

        return Response((liking_allowed, like_amount), status.HTTP_100_CONTINUE)
