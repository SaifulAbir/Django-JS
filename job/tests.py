from django.core.exceptions import ValidationError
from django.test import TestCase
from job.models import Job,Company

#COMPANY TESTS

# class CompanyTest(TestCase):
#     def when Company na6

#COMPANY TESTS

#JOB TESTS
class JobTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        s = Job(name='Software Engineer',job_location='mirpur',experience='1', gender='Male')
        try:
            s.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        s = Job(job_location='mirpur',experience='1', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        s = Job(name='',job_location='mirpur',experience='1', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_name_is_more_than_max_length_should_raise_error(self):
        s = Job(name='hsdjfdfsdhsdhsdyusdyufhdsdjdsduidiweuiduijidcsdnjdshdjuhwe'
                     'uiheduchduchsdjchsdjhchjchdhcudhfduchjcndjcndjcdjchduchsdcjxcnjcnsdcnsdcsdjlcsdjcnsdjcdhcsdhcsdckjsdncjdcndjcndjc',
                job_location='mirpur',experience='1', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_job_location_is_null_should_raise_error(self):
        s = Job(name='Software Engineer',experience='1', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_job_location_is_blank_should_raise_error(self):
        s = Job(name='Software Engineer',job_location='',experience='1', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_experience_is_null_should_raise_error(self):
        s = Job(name='Software Engineer',job_location='mirpur', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_experience_is_blank_should_raise_error(self):
        s = Job(name='Software Engineer',job_location='mirpur',experience='', gender='Male')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_gender_is_null_should_raise_error(self):
        s = Job(name='Software Engineer',job_location='mirpur')
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_when_gender_is_blank_should_raise_error(self):
        s = Job(name='Software Engineer',job_location='mirpur',experience='1', gender='')
        with self.assertRaises(ValidationError):
            s.full_clean()


#JOB TESTS