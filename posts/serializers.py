# -*- coding: utf-8 -*-
from posts.models import Post, Category
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import generics
from users.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from posts.models import Post


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['pk', 'name']


class PostSerializer(ModelSerializer):
    owner = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['pk', 'media', 'owner', 'publish_date', 'title', 'title_slug', 'summary', 'content', 'category', 'status']

    def get_fields(self):
        fields = super().get_fields()

        if 'view' in self.context:
            try:
                action = self.context['view'].action

                if self.context['view'].action in ('create', 'update'):
                    fields.pop('owner')
                    fields.pop('category')
                elif self.context['view'].action in ('list'):
                    fields.pop('status')
            except:
                # Pasará por aquí si el serializer no forma parte de un ModelViewSet, pero es necesario hacer pop de owner y category en la creación de posts
                pass

        return fields


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
