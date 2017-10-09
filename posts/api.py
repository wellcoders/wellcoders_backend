# -*- coding: utf-8 -*-
from django.http import Http404
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
    pagination_class = Pagination

    def get_queryset(self):
        if 'username' in self.request.query_params and 'title_slug' in self.request.query_params:
            user = User.objects.get(username=self.request.query_params.get('username'))
            if self.request.user.is_superuser or self.request.user == user:
                queryset = Post.objects.select_related().filter(owner=user, title_slug=self.request.query_params.
                                                                get('title_slug'))
            else:
                queryset = Post.objects.select_related().filter(owner=user, title_slug=self.request.query_params
                                                                .get('title_slug'), publish_date__lte=timezone.now(),
                                                                status=Post.PUBLISHED)
        else:
            queryset = Post.objects.select_related().filter(publish_date__lte=timezone.now(),
                                                            status=Post.PUBLISHED).all().order_by('-publish_date')

        if queryset:
            return queryset
        else:
            raise Http404

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
        try:
            username = self.kwargs.get('username', '')
            user = User.objects.get(username=username)
            return Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED,
                                                        owner=user.pk).all().order_by('-publish_date')
        except User.DoesNotExist:
            raise Http404


class CategoryPostList(ListAPIView):
    model = Post
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        category_name = self.kwargs.get('category', '')
        category = Category.objects.get(name=category_name)
        return Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED, category=category.pk).all().order_by('-publish_date')


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

