# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)

        user.set_password(validated_data.get('password'))
        user.save()

        return user


class UserDetailSerializer(ModelSerializer):

    class Meta:

        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


def login_handler(token, user=None, request=None):
    serialized_user = UserSerializer(user, context={'request': request}).data
    serialized_user.pop('password')

    return {
        'token': token,
        'user': serialized_user
    }
