from django.test import TestCase
from rest_framework.test import APIClient
from .models import BusinessOwner, Employee, Company, Review,User
from django.urls import reverse

class BusinessOwnerTests(TestCase):
    
    def setUp(self):
        data = {

            "email": "user1@example.com",
            "name": "morad",
            "password": "12345678"

        }
        user = User.objects.create_user(**data)
        self.client = APIClient()
        data = {
            "user": {
                "email": "user@example.com",
                "name": "morad",
                "password": "12345678"
            }
        }
        
        self.business_owner = BusinessOwner.objects.create(user = user)

    def test_create_business_with_exist_email(self):
        
        data = {
            "user": {
                "email": "user@example.com",
                "name": "morad",
                "password": "12345678"
            }
        }
        response = self.client.post(
            '/api/businessowners/', data, format='json')
        
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        data = {
            "email": "user1@example.com",
            "password": "12345678"
        }
        
        response = self.client.post('/login/', data,format='json')
        self.assertEqual(response.status_code, 200)


class CompanyTests(TestCase):
    
    def setUp(self):
        user1 = {

            "email": "user@example.com",
            "name": "user1",
            "password": "12345678"

        }
        user2 = {
            
                "email": "user1@example.com",
                "name": "user2",
                "password": "12345678"
            
        }
        user = User.objects.create_user(**user1)
        user2 = User.objects.create_user(**user2)
        self.client = APIClient()
       
        
        
        self.business_owner = BusinessOwner.objects.create(user = user)
        self.business_owner_2 = BusinessOwner.objects.create(user = user2)
        self.company = Company.objects.create(owner = self.business_owner,name="company1")
        self.company = Company.objects.create(owner = self.business_owner_2,name="company2")
        login_data = {
            "email": "user@example.com",
            "password": "12345678"
        }

        
        response = self.client.post('/login/', login_data, format='json')
        self.assertEqual(response.status_code, 200)

        self.token = response.data['access']

       
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_create_company_unique(self):
        #this function to test unique toghter for comapny 
        data = {
            "owner": 1,
            "name": "company1",
            "address": "Cairo"
        }
       
        response = self.client.post(
            '/api/company/', data, format='json')
        
        self.assertEqual(response.status_code, 400)

    
    def test_access_wrong_data(self):
        #this function to test bussiness owner 1 have no access for comapny 2
        
       
        response = self.client.get(
            '/api/company/2/', )
        self.assertEqual(response.status_code, 404)

    