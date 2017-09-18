# -*- coding: utf-8 -*-
from posts.models import Post
from rest_framework.serializers import ModelSerializer


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'summary', 'content', 'category']