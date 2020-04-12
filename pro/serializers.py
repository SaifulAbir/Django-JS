from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.state import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from pro.models import Professional
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from resources.strings_pro import *


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = '__all__'
class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class TokenObtainCustomSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _(ACTIVE_ACCOUNT_ERROR)
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs['email'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

class TokenObtainCustomPairSerializer(TokenObtainCustomSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        professional = Professional.objects.get(user=self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        data['full_name'] = professional.full_name
        data['professional_id'] = professional.id
        data['professional_image'] = professional.image

        return data