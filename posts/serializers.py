# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from posts.models import Post, Category, FavoritePost
from users.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from posts.models import Post, Comment


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['pk', 'name']


class PostSerializer(ModelSerializer):
    owner = UserSerializer()
    category = CategorySerializer()
    num_comments = serializers.SerializerMethodField('_num_comments')
    is_favorite = serializers.SerializerMethodField('_is_favorite')

    class Meta:
        model = Post
        fields = ['pk', 'media', 'owner', 'publish_date', 'title', 'title_slug', 'summary', 'content', 'category', 'status', 'num_comments', 'is_favorite']

    def _num_comments(self, obj):
        return Comment.objects.filter(post_id=obj).count()

    def _is_favorite(self, obj):
        if self.context['request'].user.is_authenticated():
            return FavoritePost.objects.filter(post=obj, user=self.context['request'].user).exists()
        return False

    def get_fields(self):
        fields = super().get_fields()

        if 'view' in self.context:
            try:
                action = self.context['view'].action

                if self.context['view'].action in ('create', 'update'):
                    fields.pop('owner')
                    fields.pop('category')
                    fields.pop('num_comments')
                    fields.pop('is_favorite')
            except:
                # Pasará por aquí si el serializer no forma parte de un ModelViewSet, pero es necesario hacer pop de owner y category en la creación de posts
                pass

        return fields


class CommentSerializer(ModelSerializer):
    post = PrimaryKeyRelatedField(queryset=Post.objects.all())
    owner = UserSerializer()

    class Meta:
        model = Comment
        fields = ["pk", "post", "owner", "content", "created_at"]
        write_only_fields = ["modified_at"]

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get("view")
        if view.action not in {"list", "retrieve"}:
            owner = fields.get("owner")
            owner.required = False

        return fields

    def validate_post(self, value):
        """
            Comment can not be assigned to another pos
        """

        if self.context.get("view").action in {"update", "partial_update"}:
            source_post_in_path = int(self.context.get("request").path.split("/")[-2])
            source_post_in_params = Comment.objects.filter(post__pk=value.pk).filter(pk=source_post_in_path)
            if source_post_in_params.count() == 0:
                raise serializers.ValidationError("Informed post does not belong to the user")

        return value


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

