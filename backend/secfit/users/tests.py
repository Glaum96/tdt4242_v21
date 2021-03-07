from django.test import TestCase
from users.serializers import UserSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.request import Request
from random import choice
from string import ascii_uppercase
from users.models import User
from django import forms
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model, password_validation

# Create your tests here.
"""
Tests for UserSerializers ./serializers.py
"""

class UserSerializerTestCase(TestCase):

    # Set user and serialized user data 
    def setUp(self):
        self.user_attributes = {
            "id": 1,
            "email": "email@email.com",
            "username": "user",
            "phone_number": "12345678",
            "country": "Sokovia",
            "city": "Novi Grad",
            "street_address": "Ultron Avenue",
        }

        my_factory = APIRequestFactory()
        request = my_factory.get('/')
        self.test_user = get_user_model()(**self.user_attributes)
        self.test_user.set_password("password")
        self.serialized_user = UserSerializer(
            self.test_user, context={'request': Request(request)})

        self.serializer_data = {
            "id": self.user_attributes["id"],
            "email": self.user_attributes["email"],
            "username": self.user_attributes["username"],
            "password": 'password',
            "password1": 'password',
            "athletes": [],
            "phone_number": self.user_attributes["phone_number"],
            "country": self.user_attributes["country"],
            "city": self.user_attributes["city"],
            "street_address": self.user_attributes["street_address"],
            "coach": "",
            "workouts": [],
            "coach_files": [],
            "athlete_files": [],
        }
        self.new_serializer_data = {
            "email": 'email@fake.com',
            "username": 'faker',
            "athletes": [],
            "password": 'fuck_django',
            "password1": 'fuck_django',
            "phone_number": '12345678',
            "country": 'Norge',
            "city": 'Oslo',
            "street_address": 'Mora di',
            "workouts": [],
            "coach_files": [],
            "athlete_files": [], }

    def test_validate_password(self):
        pass

    def test_create(self):
        pass

    def tearDown(self):
        return super().tearDown()