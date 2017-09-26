# -*- coding: utf-8 -*-
from posts.models import Post, Category
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from posts.models import Post
from users.serializers import UserDetailSerializer

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['pk', 'name']

class PostSerializer(ModelSerializer):
    owner = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['pk', 'media', 'owner', 'publish_date','title', 'summary', 'content', 'category']


class Pagination(PageNumberPagination):

    def get_paginated_response(self, data):
        page_size = getattr(settings, "REST_FRAMEWORK.PAGE_SIZE", 9)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'page_size': page_size,
            'count': self.page.paginator.count,
            'results': data
        })


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
