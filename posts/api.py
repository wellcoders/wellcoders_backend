# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework.generics import ListAPIView
from posts.models import Post, Category, Comment
from posts.permissions import CommentPermission
from posts.serializers import PostSerializer, CommentSerializer, Pagination, CategorySerializer
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from lxml.html.clean import clean_html


class CommentsAPI(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = Pagination
    queryset = Comment.objects.select_related().all()

    ordering = ('-created_at')

    permission_classes = (CommentPermission,)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
#        serializer.get_fields().get("owner").instance = UserSerializer(self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)



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
        title_slug = request.data.get('title_slug')

        try:
            category = Category.objects.get(pk=request.data.get('category_id'))
        except:
            pass

        if not title_slug:
            title_slug = Post.generate_title_slug(request.data.get('title'))
        else:
            title_slug = Post.generate_title_slug(request.data.get('title_slug'))

        serializer.save(owner=request.user, 
                        category=category, 
                        content=clean_html(request.data.get('content')),
                        title_slug=title_slug)

    def perform_update(self, serializer):
        request = self.request
        title_slug = request.data.get('title_slug')

        if not title_slug:
            title_slug = Post.generate_title_slug(request.data.get('title'))
        else:
            title_slug = Post.generate_title_slug(request.data.get('title_slug'))

        print(title_slug)        
        serializer.save(title_slug=title_slug)

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

