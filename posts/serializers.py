# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from posts.models import Post


class PostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
