# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from posts.models import Post


class PostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['owner', 'title', 'subtitle', 'content', 'summary', 'media', 'status', 'category']

