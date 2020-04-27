from unittest.mock import MagicMock
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import RequestsClient

from job.models import Industry
from p7.settings_dev import SITE_URL
from pro import utils
from pro.models import *

#PROFESSIONAL TESTS
class ProfessionalTest(TestCase):

    def setUp(self):
        industry = Industry(name='Information Technology')
        industry.save()
        self.industry = industry

    def test_when_everything_is_given_should_pass(self):
        professional = Professional(professional_id='1234', full_name='Peter',
                                    email='peter@any.com', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='h1234567')
        try:
            professional.full_clean()
        except:
            self.fail()

    def test_when_email_is_null_should_raise_error(self):
        professional = Professional(professional_id='1234',
                                    phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='a1234562')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_email_is_blank_should_raise_error(self):
        professional = Professional(professional_id='1234', full_name='',
                                    email='', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='a1234562')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_phone_is_null_should_raise_error(self):
        professional = Professional(full_name='Peter',
                                    email='peter@any.com', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='a1234562')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_phone_is_blank_should_raise_error(self):
        professional = Professional(professional_id='1234', full_name='Peter',
                                    email='peter@any.com', phone='', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='a1234562')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_phone_does_not_contain_number_should_raise_error(self):
        professional = Professional(full_name='Peter',
                                    email='peter@any.com', phone='0162629680d', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='a1234562')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_password_does_not_contain_number_should_raise_error(self):
        professional = Professional(full_name='Peter',
                                    email='peter@any.com', phone='01626296800', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='a')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_password_does_not_contain_character_should_raise_error(self):
        professional = Professional(full_name='Peter',
                                    email='peter@any.com', phone='01626296800', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_password_contains_special_character_should_pass(self):
        professional = Professional(full_name='Peter',
                                    email='peter@any.com', phone='01626296800', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='asd#123$')
        try:
            professional.full_clean()
        except:
            self.fail()

    def test_when_password_length_less_than_8_should_raise_error(self):
        professional = Professional(full_name='Peter',
                                    email='peter@any.com', phone='01626296800', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123abcd')
        with self.assertRaises(ValidationError):
            professional.full_clean()

# class LoginTest(TestCase):
#     def setUp(self) :
#         self.user= User()
#         self.user.email = 'test@ishraak.com'
#         self.user.username = 'test@ishraak.com'
#         self.user.password = 'abcd123@'
#
#     def testCheckProfessionalLogin_whenInputRightEmailPassword_shouldLoginSuccessfully(self):
#         email = 'test@ishraak.com'
#         password = 'abcd123@'
#         utils.checkValidEmailPassword = MagicMock(return_value=(email == self.user.username and password == self.user.password))


class ProfessionalSkillTest(TestCase):

    def setUp(self):
        skill = Skill(name='django')
        skill.save()
        self.skill = skill

        professional = Professional(email='shoab@ishraak.com',phone='01881500842',password='shoab123')
        professional.save()
        self.professional = professional


    def test__when_proper_data_is_given__professional_skill_created(self):
        url = '/api/professional/professional_skill/'
        client = RequestsClient()
        id = self.professional.id
        client.headers.update({'x-test': 'true'})
        # response = self.client.get('http://127.0.0.1:8000/api/professional/profile/'+ str(id))
        # print(response)
        skil_id = self.skill.id
        data = {'professional_id': str(id), 'skill_name_id':str(skil_id),'rating':5}
        response = client.post(SITE_URL + url, json=data, headers={'api-key': '96d56aceeb9049debeab628ac760aa11'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProfessionalSkill.objects.count(), 1)
        # self.assertEqual(ProfessionalSkill.objects.get().name, 'DabApps')


