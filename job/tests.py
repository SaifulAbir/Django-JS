from django.core.exceptions import ValidationError
from django.test import TestCase
from job.models import Job,Company,JobType,Qualification,Gender,Experience,Industry
from location.models import Division, District


#COMPANY TESTS

class CompanyTest(TestCase):
    def setUp(self) :
        division = Division(name ='Dhaka' )
        division.save()
        self.div = division

        district = District(name ='Savar', division=self.div )
        district.save()
        self.dis = district


    def test_when_everything_required_is_given_should_pass(self):
        company = Company(name='Ishraak Solutions', web_address='www.ishraak.com', division = self.div, district=self.dis)
        try:
            company.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        company = Company(web_address='www.ishraak.com', division = self.div, district=self.dis)
        with self.assertRaises(ValidationError):
            company.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        company = Company(name='', web_address='www.ishraak.com', division = self.div, district=self.dis)
        with self.assertRaises(ValidationError):
            company.full_clean()

    def test_when_district_is_null_should_pass(self):
        company = Company(name='Ishraak Solutions', web_address='www.ishraak.com',division=self.div)
        try:
            company.full_clean()
        except:
            self.fail()

    def test_when_division_is_null_should_pass(self):
        company = Company(name='Ishraak Solutions', web_address='www.ishraak.com',district=self.dis)
        try:
            company.full_clean()
        except:
            self.fail()

#COMPANY TESTS

#INDUSTRY TESTS

class IndustryTest(TestCase):

    def test_when_everything_required_is_given_should_pass(self):
        industry = Industry(name='Information Technology')
        try:
            industry.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        industry = Industry()
        with self.assertRaises(ValidationError):
            industry.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        industry = Industry(name='')
        with self.assertRaises(ValidationError):
            industry.full_clean()

    def test_when_name_is_more_than_max_length_should_raise_error(self):
        industry = Industry(name='Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                          'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, '
                          'when an unknown printer took a galley of type and scrambled it to make a type '
                          'specimen book. It has survived not only five centuries, but also the leap into '
                          'electronic typesetting, remaining essentially unchanged. It was popularised in '
                          'the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, '
                          'and more recently with desktop publishing software like Aldus PageMaker '
                          'including versions of Lorem Ipsum.')
        with self.assertRaises(ValidationError):
            industry.full_clean()

#INDUSTRY TESTS

#QUALIFICATION TESTS

class QualificationTest(TestCase):

    def test_when_everything_required_is_given_should_pass(self):
        qualification = Qualification(name='Information Technology')
        try:
            qualification.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        qualification = Qualification()
        with self.assertRaises(ValidationError):
            qualification.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        qualification = Qualification(name='')
        with self.assertRaises(ValidationError):
            qualification.full_clean()

    def test_when_name_is_more_than_max_length_should_raise_error(self):
        qualification = Qualification(name='Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                          'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, '
                          'when an unknown printer took a galley of type and scrambled it to make a type '
                          'specimen book. It has survived not only five centuries, but also the leap into '
                          'electronic typesetting, remaining essentially unchanged. It was popularised in '
                          'the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, '
                          'and more recently with desktop publishing software like Aldus PageMaker '
                          'including versions of Lorem Ipsum.')
        with self.assertRaises(ValidationError):
            qualification.full_clean()

#QUALIFICATION TESTS

#GENDER TESTS

class GenderTest(TestCase):

    def test_when_everything_required_is_given_should_pass(self):
        gender = Gender(name='Male')
        try:
            gender.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        gender = Gender()
        with self.assertRaises(ValidationError):
            gender.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        gender = Gender(name='')
        with self.assertRaises(ValidationError):
            gender.full_clean()

    def test_when_name_is_more_than_max_length_should_raise_error(self):
        gender = Gender(name='Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                          'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, '
                          'when an unknown printer took a galley of type and scrambled it to make a type '
                          'specimen book. It has survived not only five centuries, but also the leap into '
                          'electronic typesetting, remaining essentially unchanged. It was popularised in '
                          'the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, '
                          'and more recently with desktop publishing software like Aldus PageMaker '
                          'including versions of Lorem Ipsum.')
        with self.assertRaises(ValidationError):
            gender.full_clean()

#GENDER TESTS

#JOBTYPE TESTS

class JobTypeTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        company = JobType(name='Part Time')
        try:
            company.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        company = JobType()
        with self.assertRaises(ValidationError):
            company.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        company = JobType(name='')
        with self.assertRaises(ValidationError):
            company.full_clean()

#JOBTYPE TESTS

#Experience TESTS

class ExperienceTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        company = Experience(name='Part Time')
        try:
            company.full_clean()
        except:
            self.fail()

    def test_when_name_is_null_should_raise_error(self):
        company = Experience()
        with self.assertRaises(ValidationError):
            company.full_clean()

    def test_when_name_is_blank_should_raise_error(self):
        company = Experience(name='')
        with self.assertRaises(ValidationError):
            company.full_clean()


#Experience TESTS


#JOB TESTS
# class JobTest(TestCase):
#     def test_when_everything_required_is_given_should_pass(self):
#         s = Job(name='Software Engineer',job_location='mirpur',experience='1', gender='Male')
#         try:
#             s.full_clean()
#         except:
#             self.fail()
#
#     def test_when_name_is_null_should_raise_error(self):
#         s = Job(job_location='mirpur',experience='1', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_name_is_blank_should_raise_error(self):
#         s = Job(name='',job_location='mirpur',experience='1', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_name_is_more_than_max_length_should_raise_error(self):
#         s = Job(name='hsdjfdfsdhsdhsdyusdyufhdsdjdsduidiweuiduijidcsdnjdshdjuhwe'
#                      'uiheduchduchsdjchsdjhchjchdhcudhfduchjcndjcndjcdjchduchsdcjxcnjcnsdcnsdcsdjlcsdjcnsdjcdhcsdhcsdckjsdncjdcndjcndjc',
#                 job_location='mirpur',experience='1', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_job_location_is_null_should_raise_error(self):
#         s = Job(name='Software Engineer',experience='1', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_job_location_is_blank_should_raise_error(self):
#         s = Job(name='Software Engineer',job_location='',experience='1', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_experience_is_null_should_raise_error(self):
#         s = Job(name='Software Engineer',job_location='mirpur', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_experience_is_blank_should_raise_error(self):
#         s = Job(name='Software Engineer',job_location='mirpur',experience='', gender='Male')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_gender_is_null_should_raise_error(self):
#         s = Job(name='Software Engineer',job_location='mirpur')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#
#     def test_when_gender_is_blank_should_raise_error(self):
#         s = Job(name='Software Engineer',job_location='mirpur',experience='1', gender='')
#         with self.assertRaises(ValidationError):
#             s.full_clean()
#

#JOB TESTS