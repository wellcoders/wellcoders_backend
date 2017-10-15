# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, Category, Comment, FavoritePost
from posts.permissions import CommentPermission
from posts.serializers import PostSerializer, CommentSerializer, Pagination, CategorySerializer
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from lxml.html.clean import clean_html
from rest_framework import status
from rest_framework.response import Response


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
    queryset = Post.objects.all()

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
            
            if not queryset:
                raise Http404
        else:
            if 'pk' in self.kwargs:
                queryset = Post.objects.filter(pk=self.kwargs['pk'])
                
                if len(queryset) == 1 and queryset[0].owner == self.request.user:
                    return queryset
            else:
                queryset = Post.objects.select_related().filter(publish_date__lte=timezone.now(),
                                                        status=Post.PUBLISHED).all().order_by('-publish_date')
        return queryset

    def perform_create(self, serializer):
        request = self.request
        category = None
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


class UserPostList(ListAPIView):

    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        try:
            username = self.kwargs.get('username', '')
            status = self.request.GET.get('status', '')
            user = User.objects.get(username=username)

            print(user.username)
            print(self.request.user.username)

            queryset = Post.objects.select_related().filter(status=status,
                                                            owner=user).all().order_by('-publish_date')

            if user == self.request.user:
                return queryset
            else:    
                return queryset.filter(publish_date__lte=timezone.now())
            
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


class FavoritePostList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Post
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        favorite_posts = FavoritePost.objects.filter(user=self.request.user)
        print(favorite_posts.count())

        favorites = Post.objects.filter(pk__in=FavoritePost.objects.filter(user=self.request.user, 
                                                                           post__publish_date__lte=timezone.now(), 
                                                                           post__status=Post.PUBLISHED).values('post__pk')).order_by('-publish_date')

        return favorites


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FavoritePostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        queryset = Post.objects.filter(pk=post_id)

        if queryset.exists():
            post = queryset[0]

            if FavoritePost.objects.filter(user=request.user, post=post).exists():
                return Response({"favourite_post_exists": "You already have this post in your favourites"}, status=status.HTTP_409_CONFLICT) 
            else:
                FavoritePost.objects.create(user=request.user, post=post)
                return Response({"success": "Favorite saved with success"}, status=status.HTTP_201_CREATED) 
        else:
            return Response({"post_not_found": "This post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        queryset = Post.objects.filter(pk=post_id)

        if queryset.exists():
            post = queryset[0]

            if FavoritePost.objects.filter(user=request.user, post=post).exists():
                FavoritePost.objects.filter(user=request.user, post=post).delete()
                return Response({"favorite_post_deleted": "Your favorite post was deleted"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"favorite_post_not_found": "This post is not in your favourites"}, status=status.HTTP_404_NOT_FOUND) 

        else:
            return Response({"post_not_found": "This post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
