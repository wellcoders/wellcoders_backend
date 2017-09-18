# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet
from posts.models import Post
from posts.serializers import PostSerializer


class PostsAPI(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer