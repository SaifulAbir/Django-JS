from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.

#PROFESSIONAL TESTS
from job.models import Industry
from pro.models import Professional


class ProfessionalTest(TestCase):

    def setUp(self):
        industry = Industry(name='Information Technology')
        industry.save()
        self.industry = industry

    def test_when_everything_is_given_should_pass(self):
        professional = Professional(professional_id='1234', full_name='Peter', username='peter',
                                    email='peter@any.com', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123')
        try:
            professional.full_clean()
        except:
            self.fail()

    def test_when_full_name_is_null_should_raise_error(self):
        professional = Professional(professional_id='1234', username='peter',
                                    email='peter@any.com', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_full_name_is_blank_should_raise_error(self):
        professional = Professional(professional_id='1234', full_name='', username='peter',
                                    email='peter@any.com', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_professional_id_is_null_should_raise_error(self):
        professional = Professional(full_name='Peter', username='peter',
                                    email='peter@any.com', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123')
        with self.assertRaises(ValidationError):
            professional.full_clean()

    def test_when_professional_id_is_blank_should_raise_error(self):
        professional = Professional(professional_id='', full_name='Peter', username='peter',
                                    email='peter@any.com', phone='01542345678', address='Dhaka',
                                    industry_expertise=self.industry, about_me='This is Peter',
                                    password='123')
        with self.assertRaises(ValidationError):
            professional.full_clean()


