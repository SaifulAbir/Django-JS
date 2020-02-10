from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.

from location.models import Division, District


# Division tests
class DivisionTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        division = Division(name='Dhaka')
        try:
            division.full_clean()
        except:
            self.fail()

    def test_when_division_name_is_null_should_raise_error(self):
        division = Division()
        with self.assertRaises(ValidationError):
            division.full_clean()

    def test_when_division_name_is_blank_should_raise_error(self):
        division = Division(name='')
        with self.assertRaises(ValidationError):
            division.full_clean()

    def test_when_name_is_more_than_max_length_should_raise_error(self):
        division = Division(name='Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                          'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, '
                          'when an unknown printer took a galley of type and scrambled it to make a type '
                          'specimen book. It has survived not only five centuries, but also the leap into '
                          'electronic typesetting, remaining essentially unchanged. It was popularised in '
                          'the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, '
                          'and more recently with desktop publishing software like Aldus PageMaker '
                          'including versions of Lorem Ipsum.')
        with self.assertRaises(ValidationError):
            division.full_clean()
# Division tests

# District tests
class DistrictTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        district = District(name='Dhaka')
        try:
            district.full_clean()
        except:
            self.fail()

    def test_when_division_name_is_null_should_raise_error(self):
        district = Division()
        with self.assertRaises(ValidationError):
            district.full_clean()

    def test_when_division_name_is_blank_should_raise_error(self):
        district = Division(name='')
        with self.assertRaises(ValidationError):
            district.full_clean()

    def test_when_name_is_more_than_max_length_should_raise_error(self):
        district = Division(name='Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                          'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, '
                          'when an unknown printer took a galley of type and scrambled it to make a type '
                          'specimen book. It has survived not only five centuries, but also the leap into '
                          'electronic typesetting, remaining essentially unchanged. It was popularised in '
                          'the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, '
                          'and more recently with desktop publishing software like Aldus PageMaker '
                          'including versions of Lorem Ipsum.')
        with self.assertRaises(ValidationError):
            district.full_clean()
# District tests