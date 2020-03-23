from django.test import TestCase
from .models import Testimonial


#TESTIMONIAL_TEST#
class TestimonailTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        testimonial = Testimonial(name='XYZ')
        try:
            testimonial.full_clean()
        except:
            self.fail()

#SKILL TEST