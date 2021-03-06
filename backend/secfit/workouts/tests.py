"""
Tests for the workouts application.
"""
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import json

# Create your tests here.
class RegisterUsernameBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1","athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "","city": "","street_address":""}')
        self.client = APIClient()

    def test_blank_username(self):
        self.request["username"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_taken_username(self):
        self.request["username"] = "bob"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.request["email"] = "bob2@bob.no"
        request2 = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request2.status_code,400)

    def test_bad_symbols_username(self):
        self.request["username"] = "<<<"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_good_symbols_username(self):
        self.request["username"] = "@.+-"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)
        
    def test_alfanum_username(self):
        self.request["username"] = "heihei342"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class RegisterEmailBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1","athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "","city": "","street_address":""}')
        self.client = APIClient() 

    def test_blank_email(self):
        self.request["email"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_invalid_email(self):
        self.request["email"] = "bob"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_valid_email(self):
        self.request["email"] = "bob@gh.no"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_taken_email(self):
        self.request["email"] = "bob@gh.no"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.request["username"] = "bob2"
        request2 = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request2.status_code,400)


class RegisterEmailBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1,"athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "","city": "","street_address":""}')
        self.client = APIClient() 

    def test_blank_password(self):
        self.request["password"] = ""
        self.request["password1"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_length6_password(self):
        self.request["password"] = "Heihe6"
        self.request["password1"] = "Heihe6"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_length5_password(self):
        self.request["password"] = "Heih6"
        self.request["password1"] = "Heih6"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_capital_numerical_password(self):
        self.request["password"] = "Heihei1"
        self.request["password1"] = "Heihei1"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_non_capital_letter_password(self):
        self.request["password"] = "heihei1"
        self.request["password1"] = "heihei1"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_non_numerical_password(self):
        self.request["password"] = "Heiheihei"
        self.request["password1"] = "Heiheihei"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_length15_password(self):
        self.request["password"] = "Heiheiheiheihe1"
        self.request["password1"] = "Heiheiheiheihe1"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_length16_password(self):
        self.request["password"] = "Heiheiheiheihei1"
        self.request["password1"] = "Heiheiheiheihei1"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_length17_password(self):
        self.request["password"] = "Heiheiheiheihei12"
        self.request["password1"] = "Heiheiheiheihei12"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_length15_password(self):
        self.request["password"] = "Heihe6"
        self.request["password1"] = "Heihe5"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)
        
class RegisterPhonenumberBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1,"athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "","city": "","street_address":""}')
        self.client = APIClient() 
        
    def test_blank_number(self):
        self.request["phone_number"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_blank_number_twice(self):
        self.request["phone_number"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.request["email"] = "bob2@bob.no"
        self.request["username"] = "bob2"
        request2 = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request2.status_code,201)

    def test_letters_in_number(self):
        self.request["phone_number"] = "1234567A"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_length7_number(self):
        self.request["phone_number"] = "1234567"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_length8_number(self):
        self.request["phone_number"] = "12345678"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_length9_number(self):
        self.request["phone_number"] = "123456789"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_taken_number(self):
        self.request["phone_number"] = "12345678"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.request["email"] = "bob2@bob.no"
        self.request["username"] = "bob2"
        request2 = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request2.status_code,400)

class RegisterCountryBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1,"athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "hoh","city": "","street_address":""}')
        self.client = APIClient() 
        
    def test_blank_country(self):
        self.request["country"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_numerical_country(self):
        self.request["country"] = "Norway1"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,400)

    def test_space_country(self):
        self.request["country"] = "West Norway"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

class RegisterCityBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1,"athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "hoh","city": "Hello","street_address":""}')
        self.client = APIClient() 
        
    def test_blank_city(self):
        self.request["city"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_special_city(self):
        self.request["city"] = "Trond’heim #3 !"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)


class RegisterCityBoundaryTestCase(TestCase):

    def setUp(self):
        self.request = json.loads('{"username": "bob","password": "Heihei1","password1": "Heihei1,"athletes": [],"email": "bob@bob.no","coach_files": [],"athlete_files": [],"workouts":[],"phone_number": "12345678","country": "hoh","city": "Hello","street_address":"22"}')
        self.client = APIClient() 
        
    def test_blank_adress(self):
        self.request["street_address"] = ""
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    def test_special_adress(self):
        self.request["street_address"] = "Trond’heim #3 !"
        request = self.client.post('http://testserver/api/users/', json.dumps(self.request), content_type='application/json')
        self.assertEquals(request.status_code,201)

    