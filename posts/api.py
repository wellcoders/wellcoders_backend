# -*- coding: utf-8 -*-
from rest_framework.filters import SearchFilter, OrderingFilter, DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from posts.serializers import PostListSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
