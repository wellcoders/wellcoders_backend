# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from posts.models import Post, Category
from posts.serializers import PostSerializer, Pagination, CategorySerializer
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter, DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from posts.models import Post

class PostsAPI(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED).all().order_by('-publish_date')
    pagination_class = Pagination


class UserPostList(generics.ListAPIView):

    queryset = Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED).all().order_by('-publish_date')
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(owner__username=self.kwargs.get('username'))


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

