from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.


from job.models import Industry
from pro import utils
from pro.models import Professional

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


