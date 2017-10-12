# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm




class UsersListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email")

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)

        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        if(validated_data.get('password')):
            user.set_password(validated_data.get('password'))

        user.save()

        return user


def login_handler(token, user=None, request=None):
    serialized_user = UserSerializer(user, context={'request': request}).data
#    serialized_user.pop('password')

    return {
        'token': token,
        'user': serialized_user
    }


# Get the UserModel
UserModel = get_user_model()
