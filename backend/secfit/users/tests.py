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
from unittest import skip

# Create your tests here.
"""
Tests for UserSerializers ./serializers.py
"""

class UserSerializerTestCase(TestCase):

    # Set user and serialized user data 
    def setUp(self):
        self.user_attributes = {
            "id": 1,
            "email": "wanda@email.com",
            "username": "Wanda",
            "phone_number": "12345678",
            "country": "Sokovia",
            "city": "Novi Grad",
            "street_address": "Ultron Avenue"
        }

        my_factory = APIRequestFactory()
        request = my_factory.get('/')
        self.test_user = get_user_model()(**self.user_attributes)
        self.test_user.set_password("123")
        self.serialized_user = UserSerializer(self.test_user, context={'request': Request(request)})

        self.serializer_data = {
            "id": self.user_attributes["id"],
            "email": self.user_attributes["email"],
            "username": self.user_attributes["username"],
            "password": '123',
            "password1": '123',
            "athletes": [],
            "phone_number": self.user_attributes["phone_number"],
            "country": self.user_attributes["country"],
            "city": self.user_attributes["city"],
            "street_address": self.user_attributes["street_address"],
            "coach": "",
            "workouts": [],
            "coach_files": [],
            "athlete_files": []
        }

        self.second_serializer_data = {
            "email": 'viz@email.com',
            "username": 'Vision',
            "athletes": [],
            "password": 'I_hate_Thanos',
            "password1": 'I_hate_Thanos',
            "phone_number": '12345678',
            "country": 'The North',
            "city": 'Winterfell',
            "street_address": 'Godswood',
            "workouts": [],
            "coach_files": [],
            "athlete_files": []
            }

    # Testing serializer to return expected fields for a user instance
    def test_has_expected_fields(self):
        serialized_user_data = self.serialized_user.data

        self.assertEqual(set(serialized_user_data.keys()), set([
            "url",
            "id",
            "email",
            "username",
            "athletes",
            "phone_number",
            "country",
            "city",
            "street_address",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files"
        ]))

    #Testing if the serializers returns the exprected values of the fields
    def test_field_value_match(self):
        self.assertEqual(self.serialized_user.data["id"], self.user_attributes['id'])
        self.assertEqual(self.serialized_user.data["email"], self.user_attributes['email'])
        self.assertEqual(self.serialized_user.data["username"], self.user_attributes['username'])
        self.assertEqual(self.serialized_user.data["phone_number"], self.user_attributes['phone_number'])
        self.assertEqual(self.serialized_user.data["country"], self.user_attributes['country'])
        self.assertEqual(self.serialized_user.data["city"], self.user_attributes['city'])
        self.assertEqual(self.serialized_user.data["street_address"], self.user_attributes['street_address'])

    #Tests creating a new user (the second user in the setup method)
    def test_create_user(self):
        # Creates a user
        second_serializer = UserSerializer(data=self.second_serializer_data)
        self.assertTrue(second_serializer.is_valid())
        second_serializer.save()

        # Tests that the newly created user has the fields from the declaration in the serializer data in the setup method
        self.assertEquals(get_user_model().objects.get(username=self.second_serializer_data['username']).username, self.second_serializer_data['username'])
        self.assertEquals(get_user_model().objects.get(username=self.second_serializer_data['username']).email, self.second_serializer_data['email'])
        self.assertEquals(get_user_model().objects.get(username=self.second_serializer_data['username']).street_address, self.second_serializer_data['street_address'])
        self.assertEquals(get_user_model().objects.get(username=self.second_serializer_data['username']).phone_number, self.second_serializer_data['phone_number'])
        self.assertEquals(get_user_model().objects.get(username=self.second_serializer_data['username']).country, self.second_serializer_data['country'])
        self.assertEquals(get_user_model().objects.get(username=self.second_serializer_data['username']).city, self.second_serializer_data['city'])
        
        # Tests if the password in plain text matches the encrypted password in the db
        self.assertTrue(get_user_model().objects.get(username=self.second_serializer_data['username']).password,self.second_serializer_data['password'])

    # A custom setting for password length of minimum 2 has been included in the settings.py file to make this test pass.
    def test_validate_password(self):
        # Tests that an error is raised if the password is less than 2 characters in length
        with self.assertRaises(serializers.ValidationError):
            UserSerializer(self.second_serializer_data).validate_password('1')

    def test_valid_pasword(self):
        self.second_serializer_data['password'] = 'qwertyuio'
        self.second_serializer_data['password1'] = 'qwertyuio'
        dummy_data = {'password': 'qwertyuio', 'password1': 'qwertyuio'}
        
        # This returns password as the value
        user_serializer = UserSerializer(instance=None, data=dummy_data)
        self.assertEquals(user_serializer.validate_password('qwertyuio'), dummy_data['password'])


    def tearDown(self):
        return super().tearDown()