from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Settings

#TestCase_SETTINGS#
class SettingsTest(TestCase):
    def test_when_everything_required_is_given_should_pass(self):
        settings = Settings(facebook_url='https://www.facebook.com/user')
        try:
            settings.full_clean()
        except:
            self.fail()

    def test_when_facebook_url_is_null_should_raise_error(self):
        settings = Settings()
        with self.assertRaises(ValidationError):
            settings.full_clean()

    def test_when_facebook_url_is_blank_should_raise_error(self):
        settings = Settings(facebook_url='')
        with self.assertRaises(ValidationError):
            settings.full_clean()

    def test_when_not_provide_valid_url_for_facebook_should_raise_error(self):
        settings = Settings(facebook_url='dgddjah')
        with self.assertRaises(ValidationError):
            settings.full_clean()

    def test_when_not_provide_valid_url_for_linkedin_should_raise_error(self):
        settings = Settings(linkedin_url='dgddjah')
        with self.assertRaises(ValidationError):
            settings.full_clean()

    def test_when_not_provide_valid_url_for_twitter_should_raise_error(self):
        settings = Settings(twitter_url='dgddjah')
        with self.assertRaises(ValidationError):
            settings.full_clean()

#TestCase_SETTINGS#

