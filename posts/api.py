# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from posts.models import Post, Category
from posts.serializers import PostSerializer, Pagination, CategorySerializer
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter, DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from lxml.html.clean import clean_html
from posts.models import Post

class PostsAPI(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED).all().order_by('-publish_date')
    pagination_class = Pagination

    def perform_create(self, serializer):
        request = self.request
        category = None
        try:
            category = Category.objects.get(pk=request.data.get('category_id'))
        except:
            pass

        serializer.save(owner=request.user, 
                        category=category, 
                        content=clean_html(request.data.get('content')))
        

class UserPostList(ListAPIView):

    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        username = self.kwargs.get('username', '')
        user = User.objects.get(username=username)
        return Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED,
                                                    owner=user.pk).all().order_by('-publish_date')

class CategoryPostList(ListAPIView):
    model = Post
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        category_name = self.kwargs.get('category', '')
        category = Category.objects.get(name=category_name)
        return  Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED, category=category.pk).all().order_by('-publish_date')

class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
