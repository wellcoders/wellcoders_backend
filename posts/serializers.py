# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from posts.models import Post
from users.serializers import UserDetailSerializer


class PostListSerializer(ModelSerializer):

    owner = UserDetailSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(ModelSerializer):

    owner = UserDetailSerializer()

    class Meta:
        model = Post
        fields = '__all__'
