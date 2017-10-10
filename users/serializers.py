# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm



class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)

        user.set_password(validated_data.get('password'))
        user.save()

        return user


def login_handler(token, user=None, request=None):
    serialized_user = UserSerializer(user, context={'request': request}).data
   # serialized_user.pop('password')

    return {
        'token': token,
        'user': serialized_user
    }


# Get the UserModel
UserModel = get_user_model()


class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()
    print(email)
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)